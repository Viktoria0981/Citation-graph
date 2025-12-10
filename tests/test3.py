"""
Test 3 checking correctness of links.
"""

from models import Paper, Author
from graph_builder import GraphBuilder

def test_enhanced_graph_with_topic_connections():
    print("Проверка улучшенного графа")
    
    paper1 = Paper(
        paper_id="WAAAAAAA",
        title="Attention mechanism in neural networks",
        year=2019,
        citation_count=100,
        authors=[Author(name="Common Author"), Author(name="Author 1")],
        url="",
        referenced_works=[],
        source="Journal 1"
    )
    
    paper2 = Paper(
        paper_id="WBBBBBBB",
        title="Transformer models for language understanding",
        year=2021,
        citation_count=200,
        authors=[Author(name="Common Author"), Author(name="Author 2")],
        url="",
        referenced_works=[],
        source="Journal 2"
    )
    
    paper3 = Paper(
        paper_id="WCCCCCCC",
        title="Weather forecasting methods",
        year=2020,
        citation_count=50,
        authors=[Author(name="Different Author")],
        url="",
        referenced_works=[],
        source="Journal 3"
    )
    
    papers = [paper1, paper2, paper3]
    
    builder = GraphBuilder()
    basic_graph = builder.build_citation_graph(papers)
    
    print(f"Базовый граф: узлов={len(basic_graph.nodes)}, ребер={len(basic_graph.edges)}")
    
    enhanced_graph = builder.build_enhanced_citation_graph(papers)
    
    print(f"Улучшенный граф: узлов={len(enhanced_graph.nodes)}, ребер={len(enhanced_graph.edges)}")
    print(f"Ребра улучшенного графа: {enhanced_graph.edges}")
    
    connections = [
        (src, dst) for src, dst in enhanced_graph.edges 
        if {src, dst} == {"WAAAAAAA", "WBBBBBBB"}
    ]
    
    if len(connections) == 0:
        print("Не найдено связей между статьями с общим автором и темой")
    
    assert len(enhanced_graph.edges) > len(basic_graph.edges), \
        f"Улучшенный граф не добавил связи. Базовый: {len(basic_graph.edges)}, Улучшенный: {len(enhanced_graph.edges)}"
    
    print(f"Улучшенный граф добавил {len(enhanced_graph.edges) - len(basic_graph.edges)} новых связей!")

if __name__ == "__main__":
    test_enhanced_graph_with_topic_connections()
    