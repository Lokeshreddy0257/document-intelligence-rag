"""
Main RAG System orchestrator
"""
from typing import List, Dict
import os
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from rag_chain import RAGChain


class DocumentRAG:
    """Main class orchestrating the Document Intelligence RAG System"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store_manager = VectorStoreManager()
        self.rag_chain = RAGChain(self.vector_store_manager)
        self.uploaded_documents = []
    
    def upload_document(self, pdf_path: str) -> Dict[str, any]:
        """
        Upload and process a PDF document
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with upload status and document info
        """
        try:
            # Validate file exists
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"File not found: {pdf_path}")
            
            # Process the PDF
            chunks = self.document_processor.process_pdf(pdf_path)
            
            # Add to vector store
            doc_ids = self.vector_store_manager.add_documents(chunks)
            
            # Track uploaded document
            doc_info = {
                "path": pdf_path,
                "filename": os.path.basename(pdf_path),
                "chunks": len(chunks),
                "ids": doc_ids
            }
            self.uploaded_documents.append(doc_info)
            
            return {
                "status": "success",
                "message": f"Successfully processed {os.path.basename(pdf_path)}",
                "chunks_created": len(chunks),
                "document_info": doc_info
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def query(self, question: str, source_filter: str = None) -> Dict[str, any]:
        """
        Query the RAG system
        
        Args:
            question: User's question
            source_filter: Optional source document filter
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            if source_filter:
                result = self.rag_chain.query_with_filters(question, source_filter)
            else:
                result = self.rag_chain.query(question)
            
            return {
                "status": "success",
                "question": question,
                "answer": result["answer"],
                "sources": result["sources"]
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_uploaded_documents(self) -> List[Dict[str, any]]:
        """Get list of uploaded documents"""
        return self.uploaded_documents
    
    def get_collection_stats(self) -> Dict[str, any]:
        """Get statistics about the document collection"""
        return {
            "total_documents": len(self.uploaded_documents),
            "total_chunks": self.vector_store_manager.get_collection_count()
        }
    
    def reset_collection(self) -> Dict[str, any]:
        """Reset the entire document collection"""
        try:
            self.vector_store_manager.delete_collection()
            self.uploaded_documents = []
            return {
                "status": "success",
                "message": "Collection reset successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
