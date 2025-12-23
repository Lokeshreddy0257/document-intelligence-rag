"""
Document processing module for PDF text extraction and chunking
"""
from typing import List, Dict
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import config


class DocumentProcessor:
    """Handles PDF document processing and text chunking"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=config.SEPARATORS,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, any]]:
        """
        Extract text from PDF file with page metadata
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing page text and metadata
        """
        try:
            reader = PdfReader(pdf_path)
            pages_data = []
            
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text.strip():
                    pages_data.append({
                        "text": text,
                        "page": page_num,
                        "source": pdf_path
                    })
            
            return pages_data
        
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def create_chunks(self, pages_data: List[Dict[str, any]]) -> List[Document]:
        """
        Split document pages into smaller chunks with metadata
        
        Args:
            pages_data: List of page data dictionaries
            
        Returns:
            List of LangChain Document objects
        """
        documents = []
        
        for page_data in pages_data:
            # Create chunks from page text
            chunks = self.text_splitter.split_text(page_data["text"])
            
            # Create Document objects with metadata
            for chunk_idx, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": page_data["source"],
                        "page": page_data["page"],
                        "chunk": chunk_idx
                    }
                )
                documents.append(doc)
        
        return documents
    
    def process_pdf(self, pdf_path: str) -> List[Document]:
        """
        Complete pipeline: extract text and create chunks
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of chunked Document objects
        """
        pages_data = self.extract_text_from_pdf(pdf_path)
        chunks = self.create_chunks(pages_data)
        return chunks
