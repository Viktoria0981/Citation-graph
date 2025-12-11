"""
Test 2 checking the functionality of GraphBuilder.
"""

from models import Paper, Author
from graph_builder import GraphBuilder

def test_citation_graph_connectivity():
    print("Проверка построения графа цитирований")
    
    # Создаем три статьи, которые ссылаются друг на друга
    paper_a = Paper(
        paper_id="W1111111111",
        title="Paper A (cites B)",
        year=2020,
        citation_count=100,
        authors=[Author(name="Author A")],
        url="",
        referenced_works=["W2222222222"],
        source="Journal A"
    )
    
    paper_b = Paper(
        paper_id="W2222222222",
        title="Paper B (cites C)",
        year=2021,
        citation_count=200,
        authors=[Author(name="Author B")],
        url="",
        referenced_works=["W3333333333"],
        source="Journal B"
    )
    
    paper_c = Paper(
        paper_id="W3333333333",
        title="Paper C (cites A)",
        year=2022,
        citation_count=300,
        authors=[Author(name="Author C")],
        url="",
        referenced_works=["W1111111111"],
        source="Journal C"
    )
    
    papers = [paper_a, paper_b, paper_c]
    
    builder = GraphBuilder()
    graph = builder.build_citation_graph(papers)
    
    assert len(graph.nodes) == 3
    
    assert len(graph.edges) == 3
    
    edges_set = set(graph.edges)
    assert ("W1111111111", "W2222222222") in edges_set
    assert ("W2222222222", "W3333333333") in edges_set
    assert ("W3333333333", "W1111111111") in edges_set
    
    print("Граф цитирований строится корректно")

if __name__ == "__main__":
    test_citation_graph_connectivity()