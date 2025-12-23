"""
RAG Chain implementation for question answering with source citations
"""
from typing import Dict, List
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from vector_store import VectorStoreManager
import config


class RAGChain:
    """Retrieval-Augmented Generation chain for document Q&A"""
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        self.vector_store_manager = vector_store_manager
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=config.TEMPERATURE,
            openai_api_key=config.OPENAI_API_KEY
        )
        self.qa_chain = self._create_qa_chain()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for the QA chain"""
        template = """You are an AI assistant helping users understand their documents. 
Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Always cite the source document and page number when providing information.

Context:
{context}

Question: {question}

Provide a detailed answer with citations in the format [Source: filename, Page: X]:
"""
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def _create_qa_chain(self) -> RetrievalQA:
        """Create the RetrievalQA chain"""
        prompt = self._create_prompt_template()
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store_manager.vector_store.as_retriever(
                search_kwargs={"k": config.TOP_K}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        
        return qa_chain
    
    def query(self, question: str) -> Dict[str, any]:
        """
        Query the RAG system with a question
        
        Args:
            question: User's question
            
        Returns:
            Dictionary containing answer and source documents
        """
        try:
            result = self.qa_chain({"query": question})
            
            # Extract source information
            sources = self._format_sources(result["source_documents"])
            
            return {
                "answer": result["result"],
                "sources": sources,
                "source_documents": result["source_documents"]
            }
        
        except Exception as e:
            raise Exception(f"Error processing query: {str(e)}")
    
    def _format_sources(self, documents: List[Document]) -> List[Dict[str, any]]:
        """
        Format source documents into readable citations
        
        Args:
            documents: List of source documents
            
        Returns:
            List of formatted source dictionaries
        """
        sources = []
        seen = set()
        
        for doc in documents:
            metadata = doc.metadata
            source_key = (metadata.get("source", "Unknown"), metadata.get("page", "Unknown"))
            
            if source_key not in seen:
                sources.append({
                    "source": metadata.get("source", "Unknown"),
                    "page": metadata.get("page", "Unknown"),
                    "content_preview": doc.page_content[:200] + "..."
                })
                seen.add(source_key)
        
        return sources
    
    def query_with_filters(self, question: str, source_filter: str = None) -> Dict[str, any]:
        """
        Query with optional source filtering
        
        Args:
            question: User's question
            source_filter: Optional source document filter
            
        Returns:
            Dictionary containing answer and source documents
        """
        try:
            # Get relevant documents with optional filtering
            if source_filter:
                docs = self.vector_store_manager.similarity_search(
                    query=question,
                    k=config.TOP_K,
                    filter={"source": source_filter}
                )
            else:
                docs = self.vector_store_manager.similarity_search(
                    query=question,
                    k=config.TOP_K
                )
            
            # Create context from documents
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Generate answer
            prompt = self._create_prompt_template()
            formatted_prompt = prompt.format(context=context, question=question)
            
            response = self.llm.predict(formatted_prompt)
            
            sources = self._format_sources(docs)
            
            return {
                "answer": response,
                "sources": sources,
                "source_documents": docs
            }
        
        except Exception as e:
            raise Exception(f"Error processing filtered query: {str(e)}")
