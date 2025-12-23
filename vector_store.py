"""
Vector store management using ChromaDB
"""
from typing import List, Optional
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import config
import os


class VectorStoreManager:
    """Manages ChromaDB vector store for document embeddings"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY
        )
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize or load existing ChromaDB vector store"""
        # Create persist directory if it doesn't exist
        os.makedirs(config.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        
        # Initialize ChromaDB
        self.vector_store = Chroma(
            collection_name=config.COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=config.CHROMA_PERSIST_DIRECTORY
        )
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to the vector store
        
        Args:
            documents: List of Document objects to add
            
        Returns:
            List of document IDs
        """
        try:
            ids = self.vector_store.add_documents(documents)
            self.vector_store.persist()
            return ids
        except Exception as e:
            raise Exception(f"Error adding documents to vector store: {str(e)}")
    
    def similarity_search(
        self, 
        query: str, 
        k: int = config.TOP_K,
        filter: Optional[dict] = None
    ) -> List[Document]:
        """
        Perform similarity search on the vector store
        
        Args:
            query: Search query string
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of most similar documents
        """
        try:
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
            return results
        except Exception as e:
            raise Exception(f"Error performing similarity search: {str(e)}")
    
    def similarity_search_with_score(
        self, 
        query: str, 
        k: int = config.TOP_K
    ) -> List[tuple]:
        """
        Perform similarity search with relevance scores
        
        Args:
            query: Search query string
            k: Number of results to return
            
        Returns:
            List of tuples (Document, score)
        """
        try:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k
            )
            return results
        except Exception as e:
            raise Exception(f"Error performing similarity search: {str(e)}")
    
    def delete_collection(self):
        """Delete the entire collection"""
        try:
            self.vector_store.delete_collection()
            self._initialize_vector_store()
        except Exception as e:
            raise Exception(f"Error deleting collection: {str(e)}")
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection"""
        try:
            return self.vector_store._collection.count()
        except Exception as e:
            return 0
