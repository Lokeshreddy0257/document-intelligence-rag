"""
Enhanced Streamlit UI with Visualizations for Document Intelligence RAG System
"""
import streamlit as st
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from rag_system import DocumentRAG
import config

# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #00f0ff, #7000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = DocumentRAG()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'upload_history' not in st.session_state:
    st.session_state.upload_history = []
if 'query_times' not in st.session_state:
    st.session_state.query_times = []


def create_metrics_dashboard():
    """Create a metrics dashboard with visualizations"""
    stats = st.session_state.rag_system.get_collection_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📚 Total Documents",
            value=stats["total_documents"],
            delta=f"+{len(st.session_state.upload_history)} uploaded"
        )
    
    with col2:
        st.metric(
            label="🔍 Total Chunks",
            value=stats["total_chunks"],
            delta="Indexed"
        )
    
    with col3:
        st.metric(
            label="💬 Queries Answered",
            value=len(st.session_state.chat_history),
            delta="Total"
        )
    
    with col4:
        avg_time = sum(st.session_state.query_times) / len(st.session_state.query_times) if st.session_state.query_times else 0
        st.metric(
            label="⚡ Avg Response Time",
            value=f"{avg_time:.2f}s",
            delta="Fast"
        )


def create_document_distribution_chart():
    """Create a pie chart showing document distribution"""
    docs = st.session_state.rag_system.get_uploaded_documents()
    
    if docs:
        df = pd.DataFrame(docs)
        
        fig = px.pie(
            df,
            names='filename',
            values='chunks',
            title='Document Chunk Distribution',
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 Upload documents to see distribution chart")


def create_query_timeline():
    """Create a timeline of queries"""
    if st.session_state.chat_history:
        # Create timeline data
        timeline_data = []
        for idx, chat in enumerate(st.session_state.chat_history):
            timeline_data.append({
                'Query': idx + 1,
                'Question': chat['question'][:50] + '...' if len(chat['question']) > 50 else chat['question'],
                'Sources': len(chat['sources'])
            })
        
        df = pd.DataFrame(timeline_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Query'],
            y=df['Sources'],
            mode='lines+markers',
            name='Sources Used',
            line=dict(color='#00f0ff', width=3),
            marker=dict(size=10, color='#7000ff')
        ))
        
        fig.update_layout(
            title='Query Timeline - Sources Used',
            xaxis_title='Query Number',
            yaxis_title='Number of Sources',
            hovermode='x unified',
            template='plotly_dark'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📈 Ask questions to see query timeline")


def create_word_cloud():
    """Create a word cloud from all questions"""
    if st.session_state.chat_history:
        all_questions = ' '.join([chat['question'] for chat in st.session_state.chat_history])
        
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=50
        ).generate(all_questions)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Question Word Cloud', fontsize=16, fontweight='bold')
        
        st.pyplot(fig)
    else:
        st.info("☁️ Ask questions to generate word cloud")


def create_response_time_chart():
    """Create a bar chart of response times"""
    if st.session_state.query_times:
        df = pd.DataFrame({
            'Query': [f"Q{i+1}" for i in range(len(st.session_state.query_times))],
            'Time (seconds)': st.session_state.query_times
        })
        
        fig = px.bar(
            df,
            x='Query',
            y='Time (seconds)',
            title='Response Time per Query',
            color='Time (seconds)',
            color_continuous_scale='Turbo'
        )
        
        fig.update_layout(
            xaxis_title='Query',
            yaxis_title='Response Time (seconds)',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("⏱️ Query the system to see response times")


def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">📚 Document Intelligence RAG System</h1>', unsafe_allow_html=True)
    st.markdown("**Upload PDF documents and ask questions using AI-powered retrieval**")
    
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
            with st.spinner("🔄 Processing document..."):
                import time
                start_time = time.time()
                result = st.session_state.rag_system.upload_document(temp_path)
                processing_time = time.time() - start_time
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            if result["status"] == "success":
                st.success(f"✅ {result['message']}")
                st.info(f"📊 Created {result['chunks_created']} chunks in {processing_time:.2f}s")
                
                # Track upload
                st.session_state.upload_history.append({
                    'filename': uploaded_file.name,
                    'timestamp': datetime.now(),
                    'chunks': result['chunks_created']
                })
            else:
                st.error(f"❌ {result['message']}")
        
        st.divider()
        
        # Uploaded documents list
        st.header("📄 Uploaded Documents")
        docs = st.session_state.rag_system.get_uploaded_documents()
        if docs:
            for doc in docs:
                with st.expander(f"📑 {doc['filename']}"):
                    st.write(f"**Chunks:** {doc['chunks']}")
        else:
            st.info("No documents uploaded yet")
        
        st.divider()
        
        # Reset button
        if st.button("🗑️ Reset Collection", type="secondary", use_container_width=True):
            result = st.session_state.rag_system.reset_collection()
            if result["status"] == "success":
                st.session_state.chat_history = []
                st.session_state.upload_history = []
                st.session_state.query_times = []
                st.success("✅ Collection reset successfully")
                st.rerun()
    
    # Main content
    tabs = st.tabs(["💬 Chat", "📊 Analytics", "📈 Visualizations", "ℹ️ Info"])
    
    # Tab 1: Chat Interface
    with tabs[0]:
        st.header("Ask Questions")
        
        # Metrics dashboard
        create_metrics_dashboard()
        
        st.divider()
        
        # Query input
        col1, col2 = st.columns([4, 1])
        with col1:
            question = st.text_input(
                "Enter your question:",
                placeholder="What is the main topic of the document?",
                key="question_input"
            )
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            ask_button = st.button("🔍 Ask", type="primary", use_container_width=True)
        
        # Process query
        if ask_button and question:
            stats = st.session_state.rag_system.get_collection_stats()
            if stats["total_documents"] == 0:
                st.warning("⚠️ Please upload at least one document first")
            else:
                with st.spinner("🤔 Thinking..."):
                    import time
                    start_time = time.time()
                    result = st.session_state.rag_system.query(question)
                    query_time = time.time() - start_time
                
                if result["status"] == "success":
                    # Track query time
                    st.session_state.query_times.append(query_time)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": result["answer"],
                        "sources": result["sources"],
                        "time": query_time
                    })
                    
                    st.success(f"✅ Answered in {query_time:.2f}s")
                else:
                    st.error(f"❌ {result['message']}")
        
        # Display chat history
        st.divider()
        st.subheader("📝 Conversation History")
        
        for idx, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**Q{len(st.session_state.chat_history) - idx}:** {chat['question']}")
                with col2:
                    st.caption(f"⏱️ {chat['time']:.2f}s")
                
                st.markdown(f"**A:** {chat['answer']}")
                
                # Show sources
                if chat['sources']:
                    with st.expander(f"📚 View {len(chat['sources'])} Sources"):
                        for source in chat['sources']:
                            st.markdown(f"**📄 {os.path.basename(source['source'])}** - Page {source['page']}")
                            st.caption(source['content_preview'])
                            st.divider()
                
                st.divider()
    
    # Tab 2: Analytics
    with tabs[1]:
        st.header("📊 System Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Document Distribution")
            create_document_distribution_chart()
        
        with col2:
            st.subheader("Query Performance")
            create_response_time_chart()
        
        st.divider()
        
        # Upload history table
        if st.session_state.upload_history:
            st.subheader("📁 Upload History")
            upload_df = pd.DataFrame(st.session_state.upload_history)
            upload_df['timestamp'] = upload_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            st.dataframe(upload_df, use_container_width=True)
    
    # Tab 3: Visualizations
    with tabs[2]:
        st.header("📈 Interactive Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Query Timeline")
            create_query_timeline()
        
        with col2:
            st.subheader("Question Word Cloud")
            create_word_cloud()
    
    # Tab 4: Info
    with tabs[3]:
        st.header("ℹ️ How to Use")
        st.markdown("""
        ### Getting Started
        1. **Upload Documents**: Use the sidebar to upload PDF files
        2. **Ask Questions**: Type your question in the chat tab
        3. **Get Answers**: Receive AI-powered answers with source citations
        4. **View Analytics**: Check the analytics tab for insights
        
        ### Features
        - 🔍 **Semantic Search**: Advanced vector similarity search
        - 📖 **Source Attribution**: Every answer includes page numbers
        - 💬 **Conversation History**: Track all your queries
        - 📊 **Analytics Dashboard**: Visualize system performance
        - 🎯 **Context-Aware**: Maintains context across queries
        
        ### System Information
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.code(f"""
Model: {config.LLM_MODEL}
Embeddings: {config.EMBEDDING_MODEL}
Chunk Size: {config.CHUNK_SIZE}
Top-K Results: {config.TOP_K}
            """)
        
        with col2:
            st.code(f"""
Temperature: {config.TEMPERATURE}
Chunk Overlap: {config.CHUNK_OVERLAP}
Similarity Threshold: {config.SIMILARITY_THRESHOLD}
            """)
        
        st.divider()
        
        st.subheader("🎯 Tips for Best Results")
        st.markdown("""
        - Upload multiple related documents for comprehensive answers
        - Ask specific questions rather than broad queries
        - Check source citations to verify information
        - Use the analytics tab to track system performance
        - Review the word cloud to see common query patterns
        """)


if __name__ == "__main__":
    main()
