"""
FastAPI backend for Document Intelligence RAG System
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import tempfile
from rag_system import DocumentRAG
import config

app = FastAPI(
    title="Document Intelligence RAG API",
    description="RESTful API for intelligent document querying using RAG",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = DocumentRAG()


class QueryRequest(BaseModel):
    """Request model for querying"""
    question: str
    source_filter: Optional[str] = None


class QueryResponse(BaseModel):
    """Response model for queries"""
    status: str
    question: str
    answer: str
    sources: List[dict]


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Document Intelligence RAG API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload",
            "query": "/query",
            "documents": "/documents",
            "stats": "/stats"
        }
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document for processing
    
    Args:
        file: PDF file to upload
        
    Returns:
        Upload status and document information
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Check file size
    contents = await file.read()
    if len(contents) > config.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds maximum limit")
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(contents)
        tmp_path = tmp_file.name
    
    try:
        # Process the document
        result = rag_system.upload_document(tmp_path)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        
        return result
    
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Query the document collection
    
    Args:
        request: Query request with question and optional filters
        
    Returns:
        Answer with source citations
    """
    result = rag_system.query(request.question, request.source_filter)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result


@app.get("/documents")
async def get_documents():
    """Get list of uploaded documents"""
    return {
        "documents": rag_system.get_uploaded_documents()
    }


@app.get("/stats")
async def get_stats():
    """Get collection statistics"""
    return rag_system.get_collection_stats()


@app.delete("/reset")
async def reset_collection():
    """Reset the entire document collection"""
    result = rag_system.reset_collection()
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
