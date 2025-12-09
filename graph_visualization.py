"""
Graph visualization.
"""

import plotly.graph_objects as go
import networkx as nx
import plotly.express as px
from typing import Dict, List
import pandas as pd
from models import CitationGraph, Paper
from constants import COLOR_PALETTE, NODE_SIZE_RANGE, EDGE_WIDTH_RANGE


class GraphVisualizer:
    """Creates visualizations for citation graphs."""
    
    def __init__(self) -> None:
        self.color_palette = COLOR_PALETTE
    
    def create_network_plot(self, citation_graph: CitationGraph, height: int = 700) -> go.Figure:
        """
        Create interactive citation network visualization 
        """
        if not citation_graph.nodes:
            return self._create_empty_plot("No data available")
        
        G = self._build_network_for_visualization(citation_graph)
        
        if len(G.nodes) == 0:
            return self._create_empty_plot("No connected papers")
        
        pos = self._calculate_node_positions(G)
        edge_trace = self._create_edge_trace(G, pos)
        node_trace = self._create_node_trace(G, pos, citation_graph)
        label_trace = self._create_short_label_trace(G, pos, citation_graph)
        
        fig = go.Figure(data=[edge_trace, node_trace, label_trace])
        self._configure_network_layout(fig, G, height)
        
        return fig
    
    def _build_network_for_visualization(self, citation_graph: CitationGraph) -> nx.Graph:
        """Build networkx graph for visualization."""
        G = nx.DiGraph()
        
        for paper_id, paper in citation_graph.nodes.items():
            G.add_node(paper_id, 
                      title=paper.title,
                      citations=paper.citation_count,
                      year=paper.year)
        
        for citing_id, cited_id in citation_graph.edges:
            if citing_id in G.nodes and cited_id in G.nodes:
                G.add_edge(citing_id, cited_id)
        
        return G
    
    def _calculate_node_positions(self, G: nx.Graph) -> Dict[str, tuple]:
        """Calculate node positions for visualization."""
        try:
            return nx.spring_layout(G, k=2, iterations=100, seed=42)
        except Exception:
            return nx.random_layout(G, seed=42)
    
    def _create_edge_trace(self, G: nx.Graph, pos: Dict[str, tuple]) -> go.Scatter:
        """Create edge trace for network plot."""
        edge_x = []
        edge_y = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        return go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=EDGE_WIDTH_RANGE[0], color='#888', dash='dot'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        )
    
    def _create_node_trace(self, G: nx.Graph, pos: Dict[str, tuple], 
                          citation_graph: CitationGraph) -> go.Scatter:
        """Create node trace for network plot."""
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            paper = citation_graph.nodes[node]
            hover_text = self._create_hover_text(paper)
            node_text.append(hover_text)
            
            size = self._calculate_node_size(paper, citation_graph)
            node_size.append(size)
            node_color.append(paper.citation_count)
        
        return go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                size=node_size,
                color=node_color,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title="Citations",
                    thickness=15,
                    x=1.0,
                    xpad=10
                ),
                line=dict(width=2, color='darkblue')
            ),
            showlegend=False
        )
    
    def _create_short_label_trace(self, G: nx.Graph, pos: Dict[str, tuple], 
                                 citation_graph: CitationGraph) -> go.Scatter:
        """
        Create short labels - first 2-3 words + year.
        """
        label_x = []
        label_y = []
        label_text = []
        
        nodes_list = list(G.nodes())
        
        for i, node in enumerate(nodes_list):
            x, y = pos[node]
            label_x.append(x)
            label_y.append(y + 0.05)
            
            paper = citation_graph.nodes[node]
            year = paper.year or '?'
            
            words = paper.title.split()
            if len(words) <= 3:
                short_title = paper.title
            else:
                short_title = ' '.join(words[:3]) + '...'

            label_text.append(f"{short_title} ({year})")
        
        return go.Scatter(
            x=label_x, y=label_y,
            mode='text',
            text=label_text,
            textposition="top center",
            textfont=dict(
                size=9,
                color='black',
                family='Arial, sans-serif'
            ),
            hoverinfo='none',
            showlegend=False
        )
    
    def _create_hover_text(self, paper: Paper) -> str:
        """Create hover text for paper node."""
        author_names = ", ".join([str(author) for author in paper.authors[:2]])
        return (f"<b>{paper.title}</b><br>"
                f"Authors: {author_names}<br>"
                f"Year: {paper.year or 'Unknown'}<br>"
                f"Citations: {paper.citation_count}<br>"
                f"Source: {paper.source}")
    
    def _calculate_node_size(self, paper: Paper, citation_graph: CitationGraph) -> float:
        """Calculate node size"""
        max_citations = max(p.citation_count for p in citation_graph.nodes.values())
        citation_ratio = paper.citation_count / max(1, max_citations)
        
        min_size, max_size = NODE_SIZE_RANGE
        return min_size + citation_ratio * (max_size - min_size)
    
    def _configure_network_layout(self, fig: go.Figure, G: nx.Graph, height: int) -> None:
        """Configure network plot layout."""
        fig.update_layout(
            title=dict(
                text='<b>Citation Network</b><br>Papers and their citations',
                x=0.5,
                xanchor='center',
                font=dict(size=16)
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=50, l=50, r=50, t=80),
            annotations=[dict(
                text=f"Nodes: {len(G.nodes)}, Edges: {len(G.edges)}",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.02, y=0.02,
                xanchor='left',
                yanchor='bottom',
                font=dict(size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=height,
            plot_bgcolor='white'
        )
    
    def create_citations_plot(self, papers: List[Paper]) -> go.Figure:
        """Create citations by year scatter plot."""
        plot_data = self._prepare_citations_data(papers)
        
        if not plot_data:
            return self._create_empty_plot("No year data available")
        
        df = pd.DataFrame(plot_data)
        fig = px.scatter(
            df,
            x='Year',
            y='Citations',
            size='Citations',
            color='Citations',
            hover_name='Title',
            title="Citations by Publication Year",
            size_max=25,
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            xaxis_title="Publication Year",
            yaxis_title="Citation Count",
            height=500
        )
        
        return fig
    
    def create_paper_legend(self, citation_graph: CitationGraph) -> pd.DataFrame:
        """
        Create legend table with paper details.
        """
        papers_data = []
        
        for i, (paper_id, paper) in enumerate(citation_graph.nodes.items(), 1):
            papers_data.append({
                'Paper': f'P{i}',
                'Title': paper.get_short_title(60),
                'Year': paper.year or 'Unknown',
                'Citations': paper.citation_count,
                'Authors': ', '.join([str(author) for author in paper.authors[:2]])
            })
        
        return pd.DataFrame(papers_data)
    
    def _prepare_citations_data(self, papers: List[Paper]) -> List[Dict]:
        """Prepare data for citations plot."""
        plot_data = []
        
        for paper in papers:
            if paper.year and paper.citation_count > 0:
                plot_data.append({
                    'Title': paper.get_short_title(50),
                    'Year': paper.year,
                    'Citations': paper.citation_count,
                    'Authors': ', '.join([str(author) for author in paper.authors[:2]])
                })
        
        return plot_data
    
    def _create_empty_plot(self, message: str) -> go.Figure:
        """Create empty plot with message."""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
            plot_bgcolor='white',
            height=400
        )
        return fig