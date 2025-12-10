"""
Test 1 checking the functionality of the Paper.
"""

from models import Paper, Author
from graph_builder import GraphBuilder


def test_paper_model_core_functionality():
    print(" Проверка модели Paper...")
    
    paper = Paper(
        paper_id="W2758259983",
        title="Quantum Computing in the NISQ era and beyond",
        year=2018,
        citation_count=7099,
        authors=[
            Author(name="John Preskill"),
            Author(name="Co-author 1"),
            Author(name="Co-author 2")
        ],
        url="https://doi.org/10.1088/1367-2630/aa5bbc",
        referenced_works=["W1234567890", "W0987654321"],
        source="Nature"
    )
    
    assert paper.paper_id == "W2758259983"
    assert "NISQ" in paper.title
    assert paper.year == 2018
    assert paper.citation_count > 0
    assert len(paper.authors) == 3
    assert paper.authors[0].name == "John Preskill"
    assert len(paper.referenced_works) == 2
    
    # Проверяем метод get_short_title
    short_title = paper.get_short_title(40)
    assert len(short_title) > 0
    assert "Quantum" in short_title
    
    print("Модель Paper работает корректно")

if __name__ == "__main__":
    test_paper_model_core_functionality()