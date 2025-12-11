"""
Профайлинг
"""
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
from api_client import OpenAlexClient
from graph_builder import GraphBuilder
from graph_algorithms import GraphAnalyzer
from graph_visualization import GraphVisualizer
from topics import TOPICS


def print_timing(stage, start_time):
    elapsed = time.time() - start_time
    print(f"{stage:35} {elapsed:.3f} сек")
    return time.time()


def profile():
    total_start = time.time()
    checkpoint = total_start
    
    print("\nИнициализация компонентов:")
    checkpoint = print_timing("Импорт и создание объектов", checkpoint)
    
    client = OpenAlexClient()
    graph_builder = GraphBuilder()
    graph_analyzer = GraphAnalyzer()
    visualizer = GraphVisualizer()
    
    topic_key = "quantum_foundations"
    topic = TOPICS[topic_key]
    print(f"\nТема: {topic.description}")
    print(f"Запрос: {topic.query}")
    
    print("\nЗапрос к OpenAlex API:")
    try:
        papers = client.search_papers(topic, limit=15)
        checkpoint = print_timing("Поиск статей в API", checkpoint)
        print(f"Найдено статей: {len(papers)}")
    except Exception as e:
        print(f"Ошибка API: {e}")
        return
    
    if not papers:
        print("Статьи не найдены")
        return
    
    print("\nПостроение графа цитирования:")
    citation_graph = graph_builder.build_enhanced_citation_graph(papers)
    checkpoint = print_timing("Создание графа", checkpoint)
    print(f"Узлы (статьи): {len(citation_graph.nodes)}")
    print(f"Связи (цитирования): {len(citation_graph.edges)}")
    
    print("\nАнализ графа:")
    analysis_result = graph_analyzer.analyze_citation_graph(citation_graph)
    checkpoint = print_timing("Анализ метрик графа", checkpoint)
    
    metrics = analysis_result['metrics']
    print(f"Плотность графа: {metrics.get('density', 0):.4f}")
    print(f"Центральных статей найдено: {len(analysis_result['central_papers'])}")
    
    print("\nСоздание визуализаций:")
    try:
        network_plot = visualizer.create_network_plot(citation_graph)
        checkpoint = print_timing("Создание сетевого графа", checkpoint)
        
        papers_list = list(citation_graph.nodes.values())
        timeline_plot = visualizer.create_citations_plot(papers_list)
        checkpoint = print_timing("Создание графика цитирований", checkpoint)
        
        print("Визуализации созданы успешно")
    except Exception as e:
        print(f"Ошибка визуализации: {e}")
    
    print("ИТОГО:")
    
    total_time = time.time() - total_start
    print(f"Общее время выполнения: {total_time:.3f} сек")


if __name__ == "__main__":
    profile()
#Основное время (3.2 секунды) тратится на запросы к OpenAlex API. 
#Построение и анализ графа выполняются мгновенно. Визуализации занимают 0.83 секунды, особенно график цитирований.
#Оптимизировать нужно сетевые вызовы и визуализацию.