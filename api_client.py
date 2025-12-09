"""
OpenAlex API client for fetching research papers.
"""

import requests
from typing import List, Optional, Dict, Any
from models import Paper, Author, AnalysisError
from topics import TopicConfig


class OpenAlexClient:
    """Client for interacting with OpenAlex API."""
    
    BASE_URL = "https://api.openalex.org"
    TIMEOUT = 60
    
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ResearchPaperAnalyzer/1.0',
            'Accept': 'application/json'
        })
    
    def search_papers(self, topic_config: TopicConfig, limit: int = 25) -> List[Paper]:
        """
        Search for papers by topic.
        """
        url = f"{self.BASE_URL}/works"
        params = {
            'search': topic_config.query,
            'per-page': limit,
            'sort': 'cited_by_count:desc'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            return self._parse_papers_response(results)
            
        except requests.exceptions.Timeout:
            raise AnalysisError("API request timed out")
        except requests.exceptions.RequestException as e:
            raise AnalysisError(f"API request failed: {e}")
    
    def _parse_papers_response(self, results: List[Dict[str, Any]]) -> List[Paper]:
        """Parse API response into Paper objects."""
        papers: List[Paper] = []
        
        for result in results:
            paper = self._parse_single_paper(result)
            if paper:
                papers.append(paper)
        
        return papers
    
    def _parse_single_paper(self, result: Dict[str, Any]) -> Optional[Paper]:
        """Parse single paper from API response."""
        try:
            paper_id = self._extract_paper_id(result.get('id', ''))
            title = result.get('title', '')
            
            if not title or not paper_id:
                return None
            
            authors = self._parse_authors(result)
            year = self._parse_publication_year(result)
            citation_count = result.get('cited_by_count', 0)
            url = self._parse_url(result)
            referenced_works = self._parse_referenced_works(result)
            source = self._parse_source(result)
            
            return Paper(
                paper_id=paper_id,
                title=title,
                year=year,
                citation_count=citation_count,
                authors=authors,
                url=url,
                referenced_works=referenced_works,
                source=source
            )
            
        except Exception:
            return None
    
    def _parse_authors(self, result: Dict[str, Any]) -> List[Author]:
        """Parse authors from API response."""
        authors: List[Author] = []
        authorships = result.get('authorships', [])
        
        for author_data in authorships:
            author_name = author_data.get('author', {}).get('display_name', '')
            if author_name:
                authors.append(Author(name=author_name))
        
        return authors[:3]
    
    def _parse_publication_year(self, result: Dict[str, Any]) -> Optional[int]:
        """Parse publication year from API response."""
        publication_year = result.get('publication_year')
        if publication_year and str(publication_year).isdigit():
            return int(publication_year)
        return None
    
    def _parse_url(self, result: Dict[str, Any]) -> str:
        """Parse URL from API response."""
        doi = result.get('doi', '')
        return doi if doi else result.get('id', '')
    
    def _parse_referenced_works(self, result: Dict[str, Any]) -> List[str]:
        """Parse referenced works from API response."""
        referenced_works = result.get('referenced_works', [])
        if not isinstance(referenced_works, list):
            return []
        
        cleaned_refs = []
        for ref in referenced_works[:15]:
            clean_id = self._extract_paper_id(ref)
            if clean_id:
                cleaned_refs.append(clean_id)
        
        return cleaned_refs
    
    def _parse_source(self, result: Dict[str, Any]) -> str:
        """Parse source from API response."""
        source = result.get('primary_location', {}).get('source', {}).get('display_name', '')
        return source or 'Unknown'
    
    def _extract_paper_id(self, url: str) -> str:
        """Extract paper ID from OpenAlex URL."""
        if not url:
            return ""
        return url.split('/')[-1] if '/' in url else url