from abc import ABC, abstractmethod
import requests
from typing import List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.property import Property

class BaseScraper(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,ka;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    @abstractmethod
    def scrape_listings(self, search_url: str, max_pages: int = 5) -> List[Property]:
        pass
    
    @abstractmethod
    def scrape_property_details(self, property_url: str) -> Optional[Property]:
        pass
    
    def _extract_number(self, text: str) -> Optional[int]:
        if not text:
            return None
        import re
        numbers = re.findall(r'\d+', text.replace(',', '').replace(' ', ''))
        return int(numbers[0]) if numbers else None
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        return ' '.join(text.strip().split()) 