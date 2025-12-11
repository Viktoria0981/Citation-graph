"""
Data models for research paper analysis.
"""

from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Author:
    """Represents a paper author."""
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass  
class Paper:
    """Represents a scientific paper with citation data."""
    paper_id: str
    title: str
    year: Optional[int]
    citation_count: int
    authors: List[Author]
    url: Optional[str]
    referenced_works: List[str]
    source: Optional[str]
    
    def get_short_title(self, max_length: int = 80) -> str:
        """Get shortened title for display."""
        if len(self.title) > max_length:
            return self.title[:max_length] + "..."
        return self.title


@dataclass
class CitationGraph:
    """Citation graph data structure."""
    nodes: Dict[str, Paper] = field(default_factory=dict)
    edges: List[Tuple[str, str]] = field(default_factory=list)


class AnalysisError(Exception):
    """Custom exception for analysis errors."""
    pass