"""
Data models for research paper analysis.
"""

from typing import List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum


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
class TopicAnalysis:
    """Analysis results for a specific topic."""
    topic: str
    papers: List[Paper]
    total_citations: int = 0
    avg_citations: float = 0.0
    year_range: Optional[Tuple[int, int]] = None
    key_papers: List['KeyPaperAnalysis'] = field(default_factory=list)
    
    @property
    def paper_count(self) -> int:
        return len(self.papers)


class PaperSignificance(Enum):
    """Types of paper significance."""
    HIGHLY_CITED = "highly_cited"
    RECENT_BREAKTHROUGH = "recent_breakthrough" 
    TREND_SETTER = "trend_setter"
    BRIDGE_PAPER = "bridge_paper"
    FOUNDATIONAL = "foundational"


@dataclass
class KeyPaperAnalysis:
    """Analysis result for a key paper."""
    paper: Paper
    significance_tags: Set[PaperSignificance]
    citation_per_year: float
    network_centrality: Optional[float] = None
    reasons: List[str] = field(default_factory=list)


class AnalysisError(Exception):
    """Custom exception for analysis errors."""
    pass