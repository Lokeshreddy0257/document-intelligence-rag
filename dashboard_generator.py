"""
Standalone Dashboard Generator for RAG System Analytics
Creates an interactive HTML dashboard that can be opened in any browser
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import json
import os


class DashboardGenerator:
    """Generate standalone HTML dashboards for RAG analytics"""
    
    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.output_dir = "dashboards"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_full_dashboard(self, chat_history=None):
        """
        Generate a complete standalone HTML dashboard
        
        Args:
            chat_history: List of chat history dictionaries
        
        Returns:
            Path to generated HTML file
        """
        chat_history = chat_history or []
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Document Distribution',
                'Query Performance',
                'Query Timeline',
                'Response Time Distribution',
                'Source Usage',
                'System Metrics'
            ),
            specs=[
                [{"type": "pie"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "histogram"}],
                [{"type": "bar"}, {"type": "indicator"}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.15
        )
        
        # Get data
        docs = self.rag_system.get_uploaded_documents()
        stats = self.rag_system.get_collection_stats()
        
        # 1. Document Distribution (Pie Chart)
        if docs:
            doc_names = [doc['filename'] for doc in docs]
            doc_chunks = [doc['chunks'] for doc in docs]
            
            fig.add_trace(
                go.Pie(labels=doc_names, values=doc_chunks, name="Documents"),
                row=1, col=1
            )
        
        # 2. Query Performance (Bar Chart)
        if chat_history:
            query_times = [chat.get('time', 0) for chat in chat_history]
            query_labels = [f"Q{i+1}" for i in range(len(query_times))]
            
            fig.add_trace(
                go.Bar(x=query_labels, y=query_times, name="Response Time",
                       marker=dict(color=query_times, colorscale='Turbo')),
                row=1, col=2
            )
        
        # 3. Query Timeline (Line Chart)
        if chat_history:
            source_counts = [len(chat.get('sources', [])) for chat in chat_history]
            query_nums = list(range(1, len(source_counts) + 1))
            
            fig.add_trace(
                go.Scatter(x=query_nums, y=source_counts, mode='lines+markers',
                          name="Sources Used", line=dict(color='#00f0ff', width=3)),
                row=2, col=1
            )
        
        # 4. Response Time Distribution (Histogram)
        if chat_history:
            query_times = [chat.get('time', 0) for chat in chat_history]
            
            fig.add_trace(
                go.Histogram(x=query_times, name="Time Distribution",
                            marker=dict(color='#7000ff')),
                row=2, col=2
            )
        
        # 5. Source Usage (Bar Chart)
        if chat_history:
            source_counter = {}
            for chat in chat_history:
                for source in chat.get('sources', []):
                    source_name = os.path.basename(source.get('source', 'Unknown'))
                    source_counter[source_name] = source_counter.get(source_name, 0) + 1
            
            if source_counter:
                sources = list(source_counter.keys())
                counts = list(source_counter.values())
                
                fig.add_trace(
                    go.Bar(y=sources, x=counts, orientation='h', name="Source Usage",
                          marker=dict(color=counts, colorscale='Plasma')),
                    row=3, col=1
                )
        
        # 6. System Metrics (Indicator)
        avg_time = sum([chat.get('time', 0) for chat in chat_history]) / len(chat_history) if chat_history else 0
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=avg_time,
                title={'text': "Avg Response Time (s)"},
                delta={'reference': 2.0},
                gauge={
                    'axis': {'range': [None, 5]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 1], 'color': "lightgreen"},
                        {'range': [1, 2], 'color': "yellow"},
                        {'range': [2, 5], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 2.0
                    }
                }
            ),
            row=3, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Document Intelligence RAG System - Analytics Dashboard",
            title_font_size=24,
            showlegend=False,
            height=1200,
            template='plotly_dark'
        )
        
        # Save to HTML
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rag_dashboard_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        fig.write_html(
            filepath,
            config={'displayModeBar': True, 'displaylogo': False}
        )
        
        return filepath
    
    def generate_metrics_card(self):
        """Generate a simple metrics overview HTML"""
        stats = self.rag_system.get_collection_stats()
        docs = self.rag_system.get_uploaded_documents()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RAG System Metrics</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px;
                    margin: 0;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 40px;
                }}
                .metric-card {{
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    text-align: center;
                }}
                .metric-value {{
                    font-size: 3rem;
                    font-weight: bold;
                    color: #667eea;
                    margin: 10px 0;
                }}
                .metric-label {{
                    font-size: 1.2rem;
                    color: #666;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .document-list {{
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }}
                h1 {{
                    color: white;
                    text-align: center;
                    font-size: 2.5rem;
                    margin-bottom: 40px;
                }}
                h2 {{
                    color: #667eea;
                    margin-bottom: 20px;
                }}
                .doc-item {{
                    padding: 15px;
                    border-bottom: 1px solid #eee;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                .doc-item:last-child {{
                    border-bottom: none;
                }}
                .timestamp {{
                    color: white;
                    text-align: center;
                    margin-top: 20px;
                    opacity: 0.8;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 RAG System Analytics</h1>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">📚 Documents</div>
                        <div class="metric-value">{stats['total_documents']}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">🔍 Chunks</div>
                        <div class="metric-value">{stats['total_chunks']}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">📄 Avg Chunks/Doc</div>
                        <div class="metric-value">{stats['total_chunks'] // max(stats['total_documents'], 1)}</div>
                    </div>
                </div>
                
                <div class="document-list">
                    <h2>Uploaded Documents</h2>
                    {''.join([f'<div class="doc-item"><span>{doc["filename"]}</span><span>{doc["chunks"]} chunks</span></div>' for doc in docs]) if docs else '<p>No documents uploaded yet</p>'}
                </div>
                
                <div class="timestamp">
                    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                </div>
            </div>
        </body>
        </html>
        """
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"metrics_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(html)
        
        return filepath


def create_dashboard(rag_system, chat_history=None):
    """
    Convenience function to create and open dashboard
    
    Args:
        rag_system: DocumentRAG instance
        chat_history: Optional list of chat history
    
    Returns:
        Path to generated dashboard
    """
    generator = DashboardGenerator(rag_system)
    dashboard_path = generator.generate_full_dashboard(chat_history)
    
    # Auto-open in browser
    import webbrowser
    webbrowser.open('file://' + os.path.abspath(dashboard_path))
    
    return dashboard_path


if __name__ == "__main__":
    from rag_system import DocumentRAG
    
    # Example usage
    rag = DocumentRAG()
    dashboard_path = create_dashboard(rag)
    print(f"Dashboard created: {dashboard_path}")
