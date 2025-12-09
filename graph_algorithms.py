"""
Graph analysis algorithms for citation networks.
"""

import networkx as nx
from typing import Dict, List, Tuple, Any
from models import CitationGraph, Paper
from typing import List, Dict, Any, Optional, Tuple
from constants import MIN_CITATION_COUNT


class GraphAnalyzer:
    """Analyzes citation graphs using network algorithms."""
    
    def __init__(self) -> None:
        self.network_graph: Optional[nx.Graph] = None
    
    def analyze_citation_graph(self, citation_graph: CitationGraph) -> Dict[str, Any]:
        """
        Analyze citation graph and return metrics.
        """
        G = self._build_network(citation_graph)
        metrics = self._calculate_graph_metrics(G)
        central_papers = self._find_central_papers(G, citation_graph)
        
        return {
            'metrics': metrics,
            'central_papers': central_papers,
            'node_count': len(G.nodes()),
            'edge_count': len(G.edges())
        }
    
    def _build_network(self, citation_graph: CitationGraph) -> nx.Graph:
        """
        Build networkx graph from citation graph.
        """
        G = nx.DiGraph()
        
        for paper_id, paper in citation_graph.nodes.items():
            if paper.citation_count >= MIN_CITATION_COUNT:
                G.add_node(paper_id, 
                          title=paper.title,
                          year=paper.year,
                          citations=paper.citation_count)
        
        for citing_id, cited_id in citation_graph.edges:
            if citing_id in G.nodes and cited_id in G.nodes:
                G.add_edge(citing_id, cited_id)
        
        self.network_graph = G
        return G
    
    def _calculate_graph_metrics(self, G: nx.Graph) -> Dict[str, float]:
        """
        Calculate graph metrics.
        """
        if len(G) == 0:
            return {}
            
        metrics = {
            'num_nodes': G.number_of_nodes(),
            'num_edges': G.number_of_edges(),
            'density': nx.density(G),
        }
        
        try:
            degree_centrality = nx.degree_centrality(G)
            metrics['avg_degree_centrality'] = sum(degree_centrality.values()) / len(degree_centrality)
        except Exception:
            metrics['avg_degree_centrality'] = 0.0
            
        return metrics
    
    def _find_central_papers(self, G: nx.Graph, citation_graph: CitationGraph) -> List[Paper]:
        """
        Find most central papers in the graph.
        """
        if len(G) == 0:
            return []
        try:
            centrality = nx.degree_centrality(G)
            central_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
            
            central_papers = [
                citation_graph.nodes[node_id] 
                for node_id, _ in central_nodes 
                if node_id in citation_graph.nodes
            ]
            
            return central_papers
            
        except Exception:
            return []