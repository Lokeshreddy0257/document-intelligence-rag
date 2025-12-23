"""
Streamlit UI for Document Intelligence RAG System
"""
import streamlit as st
import os
from rag_system import DocumentRAG
import config

# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide"
)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = DocumentRAG()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def main():
    """Main Streamlit application"""
    
    # Header
    st.title("📚 Document Intelligence RAG System")
    st.markdown("Upload PDF documents and ask questions using AI-powered retrieval")
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Document Management")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload PDF Document",
            type=['pdf'],
            help="Upload a PDF document to add to the knowledge base"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process the document
            with st.spinner("Processing document..."):
                result = st.session_state.rag_system.upload_document(temp_path)
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            if result["status"] == "success":
                st.success(f"✅ {result['message']}")
                st.info(f"Created {result['chunks_created']} text chunks")
            else:
                st.error(f"❌ {result['message']}")
        
        st.divider()
        
        # Collection stats
        st.header("📊 Collection Stats")
        stats = st.session_state.rag_system.get_collection_stats()
        st.metric("Total Documents", stats["total_documents"])
        st.metric("Total Chunks", stats["total_chunks"])
        
        st.divider()
        
        # Uploaded documents list
        st.header("📄 Uploaded Documents")
        docs = st.session_state.rag_system.get_uploaded_documents()
        if docs:
            for doc in docs:
                st.text(f"• {doc['filename']}")
        else:
            st.info("No documents uploaded yet")
        
        st.divider()
        
        # Reset button
        if st.button("🗑️ Reset Collection", type="secondary"):
            result = st.session_state.rag_system.reset_collection()
            if result["status"] == "success":
                st.session_state.chat_history = []
                st.success("Collection reset successfully")
                st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Ask Questions")
        
        # Query input
        question = st.text_input(
            "Enter your question:",
            placeholder="What is the main topic of the document?",
            key="question_input"
        )
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            ask_button = st.button("🔍 Ask", type="primary")
        
        # Process query
        if ask_button and question:
            if stats["total_documents"] == 0:
                st.warning("⚠️ Please upload at least one document first")
            else:
                with st.spinner("Searching documents..."):
                    result = st.session_state.rag_system.query(question)
                
                if result["status"] == "success":
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": result["answer"],
                        "sources": result["sources"]
                    })
                else:
                    st.error(f"❌ {result['message']}")
        
        # Display chat history
        st.divider()
        st.subheader("📝 Conversation History")
        
        for idx, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.container():
                st.markdown(f"**Q{len(st.session_state.chat_history) - idx}:** {chat['question']}")
                st.markdown(f"**A:** {chat['answer']}")
                
                # Show sources
                if chat['sources']:
                    with st.expander("📚 View Sources"):
                        for source in chat['sources']:
                            st.markdown(f"- **{os.path.basename(source['source'])}** (Page {source['page']})")
                            st.caption(source['content_preview'])
                
                st.divider()
    
    with col2:
        st.header("ℹ️ How to Use")
        st.markdown("""
        1. **Upload Documents**: Use the sidebar to upload PDF files
        2. **Ask Questions**: Type your question in the input box
        3. **Get Answers**: Receive AI-powered answers with source citations
        4. **View Sources**: Expand source sections to see relevant excerpts
        
        ### Features
        - 🔍 Semantic search across documents
        - 📖 Source attribution with page numbers
        - 💬 Conversation history
        - 🎯 Context-aware responses
        
        ### Tips
        - Upload multiple documents for comprehensive answers
        - Ask specific questions for better results
        - Check sources to verify information
        """)
        
        st.divider()
        
        st.header("🔧 System Info")
        st.code(f"""
Model: {config.LLM_MODEL}
Embeddings: {config.EMBEDDING_MODEL}
Chunk Size: {config.CHUNK_SIZE}
Top-K Results: {config.TOP_K}
        """)


if __name__ == "__main__":
    main()
