"""
Более детальный профайлинг
"""
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cProfile
import pstats
import io
from api_client import OpenAlexClient
from graph_builder import GraphBuilder
from graph_algorithms import GraphAnalyzer
from topics import TOPICS


def profile():
    client = OpenAlexClient()
    graph_builder = GraphBuilder()
    graph_analyzer = GraphAnalyzer()
    
    topic = TOPICS["quantum_foundations"]
    
    papers = client.search_papers(topic, limit=15)
    
    if not papers:
        return None
    
    citation_graph = graph_builder.build_enhanced_citation_graph(papers)
    
    analysis_result = graph_analyzer.analyze_citation_graph(citation_graph)
    
    return analysis_result


def detailed_profile():
    pr = cProfile.Profile()
    pr.enable()
    
    result = profile()
    
    pr.disable()
    
    print("\nТоп-15 функций по времени выполнения:")
    print("-"*60)
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(15)
    
    print(s.getvalue())
    
    print("\nТоп функций по времени в самих функциях:")
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('time')
    ps.print_stats(15)
    
    print(s.getvalue())
    
    with open('profiling_results.txt', 'w') as f:
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        f.write(s.getvalue())


if __name__ == "__main__":
    detailed_profile()

# Профилирование показало, что основное время выполнения (более 95%) тратится на сетевые запросы к OpenAlex API, в частности на соединение и получение данных.
# Можно использовать параллельные запросы при загрузке данных по нескольким темам одновременно.