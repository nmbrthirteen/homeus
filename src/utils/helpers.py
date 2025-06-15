import re
from typing import Optional, List
from datetime import datetime
import hashlib

def extract_number(text: str) -> Optional[int]:
    if not text:
        return None
    numbers = re.findall(r'\d+', text.replace(',', '').replace(' ', ''))
    return int(numbers[0]) if numbers else None

def extract_float(text: str) -> Optional[float]:
    if not text:
        return None
    numbers = re.findall(r'\d+(?:\.\d+)?', text.replace(',', '').replace(' ', ''))
    return float(numbers[0]) if numbers else None

def clean_text(text: str) -> str:
    if not text:
        return ""
    return ' '.join(text.strip().split())

def normalize_currency(price_text: str) -> tuple[Optional[int], str]:
    if not price_text:
        return None, "USD"
    
    price = extract_number(price_text)
    currency = "USD"
    
    if '$' in price_text or 'USD' in price_text.upper():
        currency = "USD"
    elif '₾' in price_text or 'GEL' in price_text.upper():
        currency = "GEL"
    elif '€' in price_text or 'EUR' in price_text.upper():
        currency = "EUR"
    
    return price, currency

def generate_property_hash(title: str, price: Optional[int], location: str, size: Optional[float], rooms: Optional[int]) -> str:
    content = f"{title}{price}{location}{size}{rooms}"
    return hashlib.md5(content.encode()).hexdigest()

def is_valid_url(url: str) -> bool:
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def format_price(price: Optional[int], currency: str) -> str:
    if price is None:
        return "Price not specified"
    
    if currency == "USD":
        return f"${price:,}"
    elif currency == "GEL":
        return f"₾{price:,}"
    elif currency == "EUR":
        return f"€{price:,}"
    else:
        return f"{price:,} {currency}"

def extract_georgian_rooms(text: str) -> Optional[int]:
    if not text:
        return None
    match = re.search(r'(\d+)\s*(?:ოთახი|ოთახიანი)', text)
    return int(match.group(1)) if match else None

def extract_size_sqm(text: str) -> Optional[float]:
    if not text:
        return None
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:მ²|კვ\.მ|კვადრატული)', text)
    return float(match.group(1)) if match else None 