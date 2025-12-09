"""
Application constants.
"""

from typing import List, Tuple

OPENALEX_BASE_URL: str = "https://api.openalex.org"
REQUEST_TIMEOUT: int = 60
MAX_PAPERS_PER_TOPIC: int = 25

MAX_GRAPH_NODES: int = 50
MIN_CITATION_COUNT: int = 1
COMMUNITY_RESOLUTION: float = 1.0

COLOR_PALETTE: List[str] = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]

NODE_SIZE_RANGE: Tuple[int, int] = (15, 40)
EDGE_WIDTH_RANGE: Tuple[float, float] = (0.5, 2.0)

PAGE_TITLE: str = "Research Paper Citation Network"
PAGE_LAYOUT: str = "wide"