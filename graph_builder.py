"""
Graph builder for citation networks.
"""

from typing import List, Set
from collections import defaultdict
from models import Paper, CitationGraph


class GraphBuilder:
    """Builds citation graphs from paper data."""
    def __init__(self) -> None:
        pass
    
    def build_citation_graph(self, papers: List[Paper]) -> CitationGraph:
        """
        Build citation graph from papers.
        """
        graph = CitationGraph()
        
        paper_ids: Set[str] = set()
        for paper in papers:
            graph.nodes[paper.paper_id] = paper
            paper_ids.add(paper.paper_id)
        
        for paper in papers:
            for referenced_id in paper.referenced_works:
                if referenced_id in paper_ids:
                    graph.edges.append((paper.paper_id, referenced_id))
        
        return graph
    
    def build_enhanced_citation_graph(self, papers: List[Paper]) -> CitationGraph:
        """
        Build citation graph with enhanced connectivity.
        """
        graph = self.build_citation_graph(papers)
        
        if len(graph.edges) < max(1, len(graph.nodes) // 2):
            self._add_topic_based_edges(graph, papers)
            self._add_author_based_edges(graph, papers)
        
        return graph
    
    def _add_topic_based_edges(self, graph: CitationGraph, papers: List[Paper]) -> None:
        """Add edges between papers with similar topics/keywords."""
        keyword_to_papers = defaultdict(list)
        common_keywords = ['transformer', 'attention', 'BERT', 'GPT', 'language model', 'neural network']
        
        for paper in papers:
            title_lower = paper.title.lower()
            for keyword in common_keywords:
                if keyword in title_lower:
                    keyword_to_papers[keyword].append(paper.paper_id)
        
        for keyword, paper_ids in keyword_to_papers.items():
            if len(paper_ids) > 1:
                for i, paper1 in enumerate(paper_ids):
                    for paper2 in paper_ids[i+1:]:
                        if (paper1, paper2) not in graph.edges and (paper2, paper1) not in graph.edges:
                            graph.edges.append((paper1, paper2))
    
    def _add_author_based_edges(self, graph: CitationGraph, papers: List[Paper]) -> None:
        """Add edges between papers with common authors."""
        author_to_papers = defaultdict(list)
        
        for paper in papers:
            for author in paper.authors:
                author_to_papers[author.name].append(paper.paper_id)
        
        for author, paper_ids in author_to_papers.items():
            if len(paper_ids) > 1:
                for i, paper1 in enumerate(paper_ids):
                    for paper2 in paper_ids[i+1:]:
                        if (paper1, paper2) not in graph.edges and (paper2, paper1) not in graph.edges:
                            graph.edges.append((paper1, paper2))