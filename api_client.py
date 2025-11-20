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
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ResearchPaperAnalyzer/1.0',
            'Accept': 'application/json'
        })
        print("API Client initialized")
    
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
        
        print("=" * 50)
        print("STARTING API REQUEST")
        print("=" * 50)
        print(f"URL: {url}")
        print(f"Search query: '{topic_config.query}'")
        
        try:
            print("\nSending request to OpenAlex API...")
            response = self.session.get(url, params=params, timeout=self.TIMEOUT)
            
            print(f"Response received! Status code: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                print("No papers found for this query")
                return []
                
            print("\nParsing papers...")
            papers = self._parse_papers_response(results)
            print(f"Successfully parsed: {len(papers)} papers")

            return papers
            
        except requests.exceptions.Timeout:
            print("TIMEOUT: Request took too long (60 seconds)")
            raise AnalysisError("API request timed out")
        except requests.exceptions.RequestException as e:
            print(f"NETWORK ERROR: {e}")
            raise AnalysisError(f"API request failed: {e}")
        except (KeyError, ValueError) as e:
            print(f"PARSING ERROR: {e}")
            raise AnalysisError(f"Failed to parse API response: {e}")
    
    def _parse_papers_response(self, results: List[Dict[str, Any]]) -> List[Paper]:
        """Parse API response into Paper objects."""
        papers = []
        parse_errors = 0
        
        for i, result in enumerate(results, 1):
            try:
                paper = self._parse_single_paper(result)
                if paper:
                    papers.append(paper)
                    if i <= 3:
                        print(f"Parsed paper {i}: {paper.get_short_title(50)}")
                else:
                    parse_errors += 1
                    if i <= 3:
                        print(f"Paper {i}: Failed to parse (missing data)")
            except Exception as e:
                parse_errors += 1
                if i <= 3:
                    print(f"Paper {i}: Parse error - {e}")
                continue
        
        if parse_errors > 0:
            print(f"Failed to parse {parse_errors} papers (skipped)")
        
        return papers
    
    def _safe_get(self, data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
        """Safely get nested dictionary values."""
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            else:
                return default
            if current is None:
                return default
        return current if current is not None else default
    
    def _parse_single_paper(self, result: Dict[str, Any]) -> Optional[Paper]:
        """Parse single paper from API response."""
        try:
            paper_id = self._safe_get(result, 'id', default='')
            if paper_id:
                paper_id = paper_id.split('/')[-1]
    
            title = self._safe_get(result, 'title', default='')
            if not title or not paper_id:
                return None
            
            authors = []
            authorships = self._safe_get(result, 'authorships', default=[])
            for author_data in authorships:
                if isinstance(author_data, dict):
                    author_name = self._safe_get(author_data, 'author', 'display_name', default='')
                    if author_name:
                        authors.append(Author(name=author_name))
            
            publication_year = self._safe_get(result, 'publication_year')
            year = None
            if publication_year and str(publication_year).isdigit():
                year = int(publication_year)
            
            citation_count = self._safe_get(result, 'cited_by_count', default=0)
            
            doi = self._safe_get(result, 'doi', default='')
            openalex_url = self._safe_get(result, 'id', default='')
            url = doi if doi else openalex_url
            
            referenced_works = self._safe_get(result, 'referenced_works', default=[])
            if not isinstance(referenced_works, list):
                referenced_works = []
            
            source = self._safe_get(result, 'primary_location', 'source', 'display_name', default='Unknown')
            
            return Paper(
                paper_id=paper_id,
                title=title,
                year=year,
                citation_count=citation_count,
                authors=authors[:5],
                url=url,
                referenced_works=referenced_works[:15],
                source=source
            )
            
        except Exception as e:
            print(f"Debug: Error parsing paper - {e}")
            return None


# Это тестовый код, позже будут созданы отдельные файлы с тестами.
if __name__ == "__main__":
    print("TESTING OPENALEX API CLIENT")
    print("=" * 50)
    
    # Создаем тестовую конфигурацию темы
    test_topic = TopicConfig(
        query='quantum computer quantum processor qubit',
        description="Quantum Computing",
        color="#BB8FCE",
        category="quantum"
    )
    
    try:
        client = OpenAlexClient()
        papers = client.search_papers(test_topic, limit=10)
        
        print("\n" + "=" * 50)
        print("FINAL RESULTS")
        print("=" * 50)
        print(f"Total papers retrieved: {len(papers)}")
        
        if papers:
            # Показываем все полученные статьи
            for i, paper in enumerate(papers, 1):
                print(f"\n{i}. {paper.title}")
                print(f"   ID: {paper.paper_id}")
                print(f"   Year: {paper.year}")
                print(f"   Citations: {paper.citation_count}")
                print(f"   Source: {paper.source}")
                print(f"   Authors: {', '.join(str(a) for a in paper.authors[:3])}")
                print(f"   References: {len(paper.referenced_works)}")
                if paper.referenced_works:
                    print(f"   Sample refs: {paper.referenced_works[:2]}")
        
    except Exception as e:
        print(f"\n TEST FAILED: {e}")