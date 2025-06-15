import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import re
from datetime import datetime
import time
import logging

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper.base_scraper import BaseScraper
from models.property import Property

class SSScraper(BaseScraper):
    def __init__(self, config: dict):
        super().__init__(config['base_url'])
        self.config = config
        
    def scrape_listings(self, search_url: str, max_pages: int = 5) -> List[Property]:
        properties = []
        page = 1
        
        while page <= max_pages:
            page_url = f"{search_url}&page={page}" if 'page=' not in search_url else search_url.replace('page=1', f'page={page}')
            
            try:
                response = self.session.get(page_url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_properties = self._parse_listing_page(soup, search_url)
                
                if not page_properties:
                    break
                
                properties.extend(page_properties)
                page += 1
                time.sleep(2)
                
            except Exception as e:
                logging.error(f"Error scraping SS page {page}: {e}")
                break
        
        return properties
    
    def _parse_listing_page(self, soup: BeautifulSoup, search_url: str) -> List[Property]:
        properties = []
        
        property_cards = soup.select('.latest-item, .property-item, .listing-item, [data-id]')
        
        if not property_cards:
            property_cards = soup.select('div[class*="item"], div[class*="property"], div[class*="listing"]')
        
        for card in property_cards:
            try:
                prop = self._parse_property_card(card, search_url)
                if prop:
                    properties.append(prop)
            except Exception as e:
                logging.warning(f"Error parsing SS property card: {e}")
                continue
        
        return properties
    
    def _parse_property_card(self, card, search_url: str) -> Optional[Property]:
        try:
            title_elem = card.select_one('h3 a, .title a, a[href*="/udzravi-qoneba/"]')
            if not title_elem:
                return None
            
            title = self._clean_text(title_elem.get_text())
            
            detail_url = None
            if title_elem.get('href'):
                href = title_elem.get('href')
                detail_url = href if href.startswith('http') else f"{self.base_url}{href}"
            
            property_id = self._extract_property_id(detail_url or title)
            
            price_elem = card.select_one('.price, [class*="price"]')
            price = None
            currency = "USD"
            if price_elem:
                price_text = price_elem.get_text()
                price = self._extract_number(price_text)
                if '$' in price_text or 'USD' in price_text:
                    currency = "USD"
                elif '₾' in price_text or 'GEL' in price_text:
                    currency = "GEL"
            
            location_elem = card.select_one('.location, [class*="location"], [class*="address"]')
            location = self._clean_text(location_elem.get_text()) if location_elem else "Unknown"
            
            details_elem = card.select_one('.details, [class*="details"], .info')
            rooms = None
            size = None
            if details_elem:
                details_text = details_elem.get_text()
                rooms = self._extract_rooms(details_text)
                size = self._extract_size(details_text)
            
            image_elem = card.select_one('img')
            images = []
            if image_elem and image_elem.get('src'):
                img_src = image_elem.get('src')
                if not img_src.startswith('http'):
                    img_src = f"{self.base_url}{img_src}"
                images = [img_src]
            
            return Property(
                property_id=property_id,
                title=title,
                price=price,
                currency=currency,
                location=location,
                size=size,
                rooms=rooms,
                property_type="apartment",
                source_url=search_url,
                detail_url=detail_url,
                images=images
            )
            
        except Exception as e:
            logging.error(f"Error parsing SS property: {e}")
            return None
    
    def scrape_property_details(self, property_url: str) -> Optional[Property]:
        try:
            response = self.session.get(property_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title_elem = soup.select_one('h1, .property-title, .main-title')
            title = self._clean_text(title_elem.get_text()) if title_elem else "Unknown"
            
            price_elem = soup.select_one('.price, [class*="price"]')
            price = None
            currency = "USD"
            if price_elem:
                price_text = price_elem.get_text()
                price = self._extract_number(price_text)
                if '$' in price_text or 'USD' in price_text:
                    currency = "USD"
                elif '₾' in price_text or 'GEL' in price_text:
                    currency = "GEL"
            
            description_elem = soup.select_one('.description, [class*="description"]')
            description = self._clean_text(description_elem.get_text()) if description_elem else None
            
            all_text = soup.get_text()
            size = self._extract_size(all_text)
            rooms = self._extract_rooms(all_text)
            
            location_elem = soup.select_one('.location, [class*="location"], [class*="address"]')
            location = self._clean_text(location_elem.get_text()) if location_elem else "Tbilisi"
            
            images = []
            img_elements = soup.select('.gallery img, .images img, .property-images img')
            for img in img_elements:
                if img.get('src'):
                    img_src = img.get('src')
                    if not img_src.startswith('http'):
                        img_src = f"{self.base_url}{img_src}"
                    images.append(img_src)
            
            property_id = self._extract_property_id(property_url)
            
            return Property(
                property_id=property_id,
                title=title,
                price=price,
                currency=currency,
                location=location,
                size=size,
                rooms=rooms,
                property_type="apartment",
                description=description,
                source_url=property_url,
                detail_url=property_url,
                images=images
            )
            
        except Exception as e:
            logging.error(f"Error scraping SS property details: {e}")
            return None
    
    def _extract_property_id(self, url_or_text: str) -> str:
        if not url_or_text:
            return f"ss_{hash(url_or_text) % 1000000}"
        
        match = re.search(r'/udzravi-qoneba/[^/]+-(\d+)', url_or_text)
        if match:
            return f"ss_{match.group(1)}"
        
        return f"ss_{hash(url_or_text) % 1000000}"
    
    def _extract_rooms(self, text: str) -> Optional[int]:
        if not text:
            return None
        match = re.search(r'(\d+)\s*(?:ოთახი|otaxi|room)', text.lower())
        return int(match.group(1)) if match else None
    
    def _extract_size(self, text: str) -> Optional[float]:
        if not text:
            return None
        
        patterns = [
            r'ფართი\s*(\d+(?:\.\d+)?)\s*m²',
            r'ფართი\s*(\d+(?:\.\d+)?)\s*მ²',
            r'(\d{2,3}(?:\.\d+)?)\s*m²',
            r'(\d{2,3}(?:\.\d+)?)\s*მ²',
            r'(\d+(?:\.\d+)?)\s*კვ\.?\s*მ',
            r'(\d+(?:\.\d+)?)\s*sqm',
            r'(\d+(?:\.\d+)?)\s*sq\.?\s*m',
            r'(\d+(?:\.\d+)?)\s*კვადრატული\s*მეტრი'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                sizes = [float(m) for m in matches if float(m) > 10]
                if sizes:
                    return max(sizes)
        return None 