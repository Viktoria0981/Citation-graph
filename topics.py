# topics.py
from dataclasses import dataclass
from enum import Enum

class TopicCategory(Enum):
    QUANTUM = "quantum"
    ENERGY = "energy" 
    MEDICAL = "medical"
    NEUROSCIENCE = "neuroscience"
    SUSTAINABILITY = "sustainability"
    AI = "artificial_intelligence"

@dataclass
class TopicConfig:
    query: str
    description: str
    color: str
    category: TopicCategory

TOPICS = {
    "quantum_computing": TopicConfig(
        # Более специфичный запрос для квантовых вычислений
        query='(quantum computing) OR (quantum computer) OR (quantum processor) OR (qubit) OR (quantum algorithm) OR (quantum circuit)',
        description="Quantum Computing",
        color="#BB8FCE",
        category=TopicCategory.QUANTUM
    ),
    
    "quantum_computing_specific": TopicConfig(
        # Альтернативный очень специфичный запрос
        query='"quantum computing" "quantum computer" qubit "quantum algorithm" "quantum hardware"',
        description="Quantum Computing (Specific)",
        color="#9B59B6", 
        category=TopicCategory.QUANTUM
    ),
    
    "battery_tech": TopicConfig(
        query="solid state lithium battery energy density",
        description="Next-Gen Batteries", 
        color="#F7DC6F",
        category=TopicCategory.ENERGY
    ),
    
    "ai_neuroscience": TopicConfig(
        query="deep learning fMRI classification",
        description="AI in Neuroscience",
        color="#5DADE2",
        category=TopicCategory.NEUROSCIENCE
    ),
}
#Вероятно темы будут еще изменены (и добавлены), когда я начну строить графы, чтобы получились наиболее наглядными)
#Также на тестах надо будет проверить, чтобы сервер возращал подходящие под мою тему статьи (может быть стоит поменять ключевые слова для отправляемых запросов)