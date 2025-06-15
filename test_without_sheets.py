#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.scraper.myhome_scraper import MyHomeScraper
from src.scraper.ss_scraper import SSScraper
from src.models.property import Property
from src.storage.database import Database
from src.utils.config import load_config

def test_without_sheets():
    print("🏠 Testing Homeus Core Functionality (without Google Sheets)...")
    
    try:
        config = load_config('config/config.yaml')
        config['google_sheets']['enabled'] = False
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    db = Database('data/homeus.db')
    print("✅ Database initialized")
    
    total_new_properties = 0
    
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
                print(f"  📋 Scraping: {search_config['name']}")
                
                properties = scraper.scrape_listings(search_config['url'], max_pages=2)
                print(f"  📊 Found {len(properties)} properties")
                
                new_count = 0
                for prop in properties:
                    if db.is_new_property(prop.property_id):
                        if db.save_property(prop):
                            new_count += 1
                            print(f"    ✅ New: {prop.title[:50]}... - {prop.price} {prop.currency}")
                        else:
                            print(f"    ❌ Failed to save: {prop.property_id}")
                    else:
                        db.update_property_last_seen(prop.property_id)
                
                print(f"  📈 New properties saved: {new_count}")
                total_new_properties += new_count
                
        except Exception as e:
            print(f"  ❌ Error testing {site_name}: {e}")
    
    stats = db.get_stats()
    print(f"\n📈 Final Database Stats:")
    print(f"  Total properties: {stats['total_properties']}")
    print(f"  Today's properties: {stats['today_properties']}")
    print(f"  New properties this run: {total_new_properties}")
    
    print(f"\n🎉 Core functionality test completed!")
    print(f"📝 Next step: Set up Google Sheets integration using GOOGLE_SHEETS_SETUP.md")
    return True

if __name__ == "__main__":
    test_without_sheets() 