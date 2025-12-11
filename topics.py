"""
Topics configuration.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class TopicConfig:
    """Configuration for research topics."""
    query: str
    description: str
    color: str
    category: str


TOPICS: Dict[str, TopicConfig] = {
    "quantum_foundations": TopicConfig(
        query='("quantum supremacy" OR "NISQ era" OR "variational quantum" OR VQE OR QAOA)',
        description="Quantum Computing Foundations", 
        color="#4ECDC4",
        category="quantum"
    ),
    "crispr_cas9": TopicConfig(
    query='CRISPR AND Cas9 AND ("gene editing" OR Doudna OR Charpentier)',
    description="CRISPR-Cas9 Gene Editing", 
    color="#2C3837",
    category="biotechnology"
)
}