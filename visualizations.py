"""
Visualization utilities for the RAG system
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
import pandas as pd


class RAGVisualizer:
    """Visualization utilities for RAG system analytics"""
    
    @staticmethod
    def create_similarity_heatmap(query: str, documents: List[Dict], scores: List[float]):
        """
        Create a heatmap showing similarity scores between query and documents
        
        Args:
            query: The search query
            documents: List of document metadata
            scores: Similarity scores for each document
        """
        doc_names = [f"Doc {i+1}" for i in range(len(documents))]
        
        fig = go.Figure(data=go.Heatmap(
            z=[scores],
            x=doc_names,
            y=['Similarity'],
            colorscale='Viridis',
            text=[[f"{score:.3f}" for score in scores]],
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Score")
        ))
        
        fig.update_layout(
            title=f'Document Similarity Scores for: "{query[:50]}..."',
            xaxis_title='Documents',
            height=300
        )
        
        return fig
    
    @staticmethod
    def create_chunk_distribution(documents: List[Dict]):
        """
        Create a bar chart showing chunk distribution across documents
        """
        df = pd.DataFrame(documents)
        
        fig = px.bar(
            df,
            x='filename',
            y='chunks',
            title='Text Chunks per Document',
            labels={'filename': 'Document', 'chunks': 'Number of Chunks'},
            color='chunks',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_source_usage_chart(chat_history: List[Dict]):
        """
        Create a chart showing which sources are used most frequently
        """
        source_counter = {}
        
        for chat in chat_history:
            for source in chat.get('sources', []):
                source_name = source.get('source', 'Unknown')
                source_counter[source_name] = source_counter.get(source_name, 0) + 1
        
        if not source_counter:
            return None
        
        df = pd.DataFrame(
            list(source_counter.items()),
            columns=['Source', 'Usage Count']
        )
        df = df.sort_values('Usage Count', ascending=True)
        
        fig = px.bar(
            df,
            x='Usage Count',
            y='Source',
            orientation='h',
            title='Most Referenced Sources',
            color='Usage Count',
            color_continuous_scale='Plasma'
        )
        
        fig.update_layout(
            yaxis_title='',
            xaxis_title='Number of Times Referenced',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_performance_gauge(avg_response_time: float, target_time: float = 2.0):
        """
        Create a gauge chart for response time performance
        """
        # Calculate performance percentage (inverse - lower time is better)
        performance = min(100, (target_time / avg_response_time) * 100) if avg_response_time > 0 else 100
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_response_time,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Avg Response Time (seconds)"},
            delta={'reference': target_time},
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
                    'value': target_time
                }
            }
        ))
        
        fig.update_layout(height=300)
        
        return fig
    
    @staticmethod
    def create_query_length_distribution(chat_history: List[Dict]):
        """
        Create a histogram of query lengths
        """
        query_lengths = [len(chat['question'].split()) for chat in chat_history]
        
        fig = px.histogram(
            x=query_lengths,
            nbins=10,
            title='Query Length Distribution',
            labels={'x': 'Number of Words', 'y': 'Frequency'},
            color_discrete_sequence=['#00f0ff']
        )
        
        fig.update_layout(
            xaxis_title='Query Length (words)',
            yaxis_title='Number of Queries',
            showlegend=False
        )
        
        return fig
