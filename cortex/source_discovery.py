"""
External Source Discovery Module
Finds and fetches relevant external content
"""

import re
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


class SourceDiscovery:
    """Discovers and fetches external sources"""
    
    # Maximum content length to store from external sources
    MAX_CONTENT_LENGTH = 5000
    
    def __init__(self, max_sources: int = 5):
        """
        Initialize the source discovery engine
        
        Args:
            max_sources: Maximum number of external sources to fetch
        """
        self.max_sources = max_sources
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; CortexKB/0.1)'
        })
    
    def extract_urls_from_text(self, text: str) -> List[str]:
        """
        Extract URLs from text
        
        Args:
            text: Text to extract URLs from
            
        Returns:
            List of URLs found in the text
        """
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text)
        return urls
    
    def fetch_url_content(self, url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
        """
        Fetch content from a URL
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary with URL content and metadata, or None if failed
        """
        try:
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Extract title
            title = soup.find('title')
            title_text = title.string if title else urlparse(url).netloc
            
            return {
                'url': url,
                'title': title_text,
                'content': text[:self.MAX_CONTENT_LENGTH],  # Limit content length
                'type': 'web',
                'source': 'external'
            }
        
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def discover_related_sources(
        self, 
        text: str, 
        existing_urls: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Discover and fetch related external sources
        
        Args:
            text: Text to find related sources for
            existing_urls: URLs already in the knowledge base
            
        Returns:
            List of fetched source documents
        """
        if existing_urls is None:
            existing_urls = []
        
        # Extract URLs from text
        found_urls = self.extract_urls_from_text(text)
        
        # Filter out already existing URLs
        new_urls = [url for url in found_urls if url not in existing_urls]
        
        # Limit to max_sources
        new_urls = new_urls[:self.max_sources]
        
        # Fetch content from each URL
        sources = []
        for url in new_urls:
            content = self.fetch_url_content(url)
            if content:
                sources.append(content)
        
        return sources
    
    def search_web(self, query: str) -> List[Dict[str, Any]]:
        """
        Placeholder for web search functionality
        In a real implementation, this would integrate with a search API
        
        Args:
            query: Search query
            
        Returns:
            List of search results (currently returns empty list)
        """
        # This is a placeholder - in a production system, you would integrate
        # with a search API like Google Custom Search, Bing, or DuckDuckGo
        print(f"Web search for '{query}' - feature placeholder")
        return []
    
    def vet_source(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """
        Vet a source for quality and relevance
        
        Args:
            source: Source document to vet
            
        Returns:
            Source with added quality metrics
        """
        quality_score = 0.5  # Base score
        
        # Check content length (longer is often better quality)
        content = source.get('content', '')
        if len(content) > 1000:
            quality_score += 0.2
        elif len(content) > 500:
            quality_score += 0.1
        
        # Check if it has a proper title
        if source.get('title') and len(source.get('title', '')) > 10:
            quality_score += 0.1
        
        # Check URL quality (e.g., avoid suspicious domains)
        url = source.get('url', '')
        if any(domain in url for domain in ['.edu', '.gov', '.org']):
            quality_score += 0.2
        
        # Cap at 1.0
        quality_score = min(1.0, quality_score)
        
        return {
            **source,
            'quality_score': quality_score,
            'vetted': True
        }
