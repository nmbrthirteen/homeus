#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.scraper.myhome_scraper import MyHomeScraper
from src.scraper.ss_scraper import SSScraper
from src.models.property import Property
from src.storage.database import Database
from src.utils.config import load_config

def test_scrapers():
    print("🏠 Testing Homeus Scrapers...")
    
    try:
        config = load_config('config/config.yaml')
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    db = Database('data/test.db')
    print("✅ Database initialized")
    
    for site_name, site_config in config['websites'].items():
        print(f"\n🔍 Testing {site_name.upper()} scraper...")
        
        try:
            if site_name == 'myhome':
                scraper = MyHomeScraper(site_config)
            elif site_name == 'ss':
                scraper = SSScraper(site_config)
            else:
                continue
            
            for search_config in site_config['search_urls']:
                print(f"  📋 Testing: {search_config['name']}")
                
                properties = scraper.scrape_listings(search_config['url'], max_pages=1)
                print(f"  📊 Found {len(properties)} properties")
                
                if properties:
                    sample_prop = properties[0]
                    print(f"  🏡 Sample: {sample_prop.title[:50]}...")
                    print(f"  💰 Price: {sample_prop.price} {sample_prop.currency}")
                    print(f"  📍 Location: {sample_prop.location}")
                    
                    if db.save_property(sample_prop):
                        print("  ✅ Database save successful")
                    else:
                        print("  ❌ Database save failed")
                
        except Exception as e:
            print(f"  ❌ Error testing {site_name}: {e}")
    
    stats = db.get_stats()
    print(f"\n📈 Database Stats:")
    print(f"  Total properties: {stats['total_properties']}")
    print(f"  Today's properties: {stats['today_properties']}")
    
    print("\n🎉 Test completed!")
    return True

if __name__ == "__main__":
    test_scrapers() 