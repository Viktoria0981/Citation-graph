"""
Streamlit web interface for research paper analysis.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List

from api_client import OpenAlexClient
from graph_builder import GraphBuilder
from graph_algorithms import GraphAnalyzer
from graph_visualization import GraphVisualizer
from topics import TOPICS, TopicConfig
from models import Paper, CitationGraph
from constants import PAGE_TITLE, PAGE_LAYOUT


def setup_page() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        layout=PAGE_LAYOUT,
        initial_sidebar_state="expanded"
    )


def render_sidebar() -> TopicConfig:
    """
    Render sidebar and return selected topic.
    """
    st.sidebar.title("Research Topics")
    st.sidebar.markdown("Select a research topic to analyze:")
    
    topic_keys = list(TOPICS.keys())
    topic_descriptions = [TOPICS[key].description for key in topic_keys]
    
    selected_topic_desc = st.sidebar.selectbox(
        "Choose Topic:",
        topic_descriptions,
        index=0
    )
    
    selected_topic_key = topic_keys[topic_descriptions.index(selected_topic_desc)]
    selected_topic = TOPICS[selected_topic_key]
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Query:** `{selected_topic.query}`")
    st.sidebar.markdown(f"**Category:** {selected_topic.category}")
    
    return selected_topic


def render_header(topic: TopicConfig) -> None:
    """
    Render page header.
    """
    st.title("Research Paper Citation Network")
    st.markdown(f"### Analyzing: **{topic.description}**")
    st.markdown("---")


def render_papers_table(papers: List[Paper]) -> None:
    """
    Render papers data table.
    """
    if not papers:
        st.warning("No papers found for this topic.")
        return
    
    table_data = []
    for paper in papers:
        table_data.append({
            'Title': paper.get_short_title(70),
            'Year': paper.year or 'Unknown',
            'Citations': paper.citation_count,
            'Authors': ', '.join(str(author) for author in paper.authors[:2]),
            'Source': paper.source or 'Unknown'
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)


def render_graph_metrics(metrics: Dict[str, float]) -> None:
    """
    Render graph metrics as columns.
    """
    if not metrics:
        return
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Papers", int(metrics.get('num_nodes', 0)))
    with col2:
        st.metric("Citations", int(metrics.get('num_edges', 0)))


def render_network_graph(visualizer: GraphVisualizer, citation_graph: CitationGraph) -> None:
    """
    Render network graph visualization.
    """
    try:
        fig_network = visualizer.create_network_plot(citation_graph)
        st.plotly_chart(fig_network, use_container_width=True)
        
        with st.expander("How to interpret this graph:"):
            st.markdown("""
            - **Nodes**: Research papers
            - **Size**: Citation count (larger = more citations)
            - **Color**: Citation count (darker = more citations)  
            - **Edges**: Citation relationships
            - **Hover**: See paper details
            """)
            
    except Exception as e:
        st.error(f"Network visualization error: {str(e)}")


def render_key_papers(central_papers: List[Paper]) -> None:
    """
    Render key papers section.
    """
    if not central_papers:
        return
    
    st.subheader("Key Influential Papers")
    st.markdown("These papers are central in the citation network:")
    
    for i, paper in enumerate(central_papers, 1):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{i}. {paper.title}**")
                st.caption(f"Authors: {', '.join(str(author) for author in paper.authors[:2])}")
            
            with col2:
                st.metric("Citations", paper.citation_count)
                st.metric("Year", paper.year or "Unknown")
            
            st.markdown("---")


def main():
    setup_page()
    
    try:
        client = OpenAlexClient()
        graph_builder = GraphBuilder()
        graph_analyzer = GraphAnalyzer()
        visualizer = GraphVisualizer()
        
        selected_topic = render_sidebar()
        
        render_header(selected_topic)
        
        with st.spinner('Fetching research papers from OpenAlex...'):
            papers = client.search_papers(selected_topic)
        
        if not papers:
            st.error("No papers found. Please try a different topic.")
            return
        
        st.subheader(f"Found {len(papers)} Research Papers")
        render_papers_table(papers)
        
        with st.spinner('Building citation network...'):
            citation_graph = graph_builder.build_enhanced_citation_graph(papers)
        
        with st.spinner('Analyzing network...'):
            analysis_result = graph_analyzer.analyze_citation_graph(citation_graph)
        
        st.subheader("Citation Network Analysis")
        
        if not citation_graph.nodes:
            st.warning("No papers available for graph analysis.")
            return
        
        render_graph_metrics(analysis_result['metrics'])
        
        tab1, tab2 = st.tabs(["Network Graph", "Citations Timeline"])
        
        with tab1:
            render_network_graph(visualizer, citation_graph)
            with st.expander("Paper Details Table"):
                st.markdown("""
                **Paper details corresponding to labels on the graph:**
                - **Paper**: Paper identifier (P1, P2, etc.)
                - **Title**: Full paper title (shortened)
                - **Year**: Publication year
                - **Citations**: Number of citations
                - **Authors**: Main authors
                """)
                legend_df = visualizer.create_paper_legend(citation_graph)
                st.dataframe(legend_df, use_container_width=True)
        
        with tab2:
            papers_list = list(citation_graph.nodes.values())
            fig_timeline = visualizer.create_citations_plot(papers_list)
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        render_key_papers(analysis_result['central_papers'])
        
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please try again")


if __name__ == "__main__":
    main()