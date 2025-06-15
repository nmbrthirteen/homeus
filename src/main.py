import schedule
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scraper.myhome_scraper import MyHomeScraper
from scraper.ss_scraper import SSScraper
from storage.database import Database
from storage.sheets_manager import SheetsManager
from utils.logger import setup_logger
from utils.config import load_config

class HomeusManager:
    def __init__(self, config_path: str):
        self.config = load_config(config_path)
        self.logger = setup_logger(self.config['logging'])
        self.db = Database(self.config['database']['path'])
        self.sheets = SheetsManager(self.config['google_sheets']) if self.config['google_sheets']['enabled'] else None
        self.scrapers = self._init_scrapers()
        
    def _init_scrapers(self):
        scrapers = {}
        for site_name, site_config in self.config['websites'].items():
            if site_name == 'myhome':
                scrapers[site_name] = MyHomeScraper(site_config)
            elif site_name == 'ss':
                scrapers[site_name] = SSScraper(site_config)
        return scrapers
    
    def run_scraping_cycle(self):
        self.logger.info("Starting scraping cycle")
        session_id = self.db.start_scraping_session()
        
        try:
            new_properties_count = 0
            total_properties_count = 0
            
            for site_name, scraper in self.scrapers.items():
                site_config = self.config['websites'][site_name]
                
                for search_config in site_config['search_urls']:
                    self.logger.info(f"Scraping: {search_config['name']}")
                    
                    properties = scraper.scrape_listings(
                        search_config['url'], 
                        max_pages=self.config['scraping'].get('max_pages', 5)
                    )
                    total_properties_count += len(properties)
                    
                    for prop in properties:
                        if self.db.is_new_property(prop.property_id):
                            if prop.detail_url:
                                try:
                                    detailed_prop = scraper.scrape_property_details(prop.detail_url)
                                    if detailed_prop:
                                        prop = detailed_prop
                                except Exception as e:
                                    self.logger.warning(f"Failed to get details for {prop.property_id}: {e}")
                            
                            self.db.save_property(prop)
                            
                            if self.sheets:
                                self.sheets.add_property(prop)
                            
                            new_properties_count += 1
                            self.logger.info(f"New property: {prop.title} - {prop.price} {prop.currency}")
                        else:
                            self.db.update_property_last_seen(prop.property_id)
            
            self.db.finish_scraping_session(session_id, total_properties_count, new_properties_count)
            self.logger.info(f"Cycle completed. Found {total_properties_count} properties, {new_properties_count} new")
            
        except Exception as e:
            self.db.finish_scraping_session(session_id, 0, 0, str(e))
            self.logger.error(f"Scraping cycle failed: {e}")
    
    def start_monitoring(self):
        self.logger.info("Starting Homeus monitoring...")
        
        schedule.every(self.config['scraping']['interval_minutes']).minutes.do(self.run_scraping_cycle)
        
        self.run_scraping_cycle()
        
        while True:
            schedule.run_pending()
            time.sleep(30)

def main():
    parser = argparse.ArgumentParser(description='Homeus Property Scraper')
    parser.add_argument('--config', default='config/config.yaml', help='Configuration file path')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    
    args = parser.parse_args()
    
    try:
        manager = HomeusManager(args.config)
        
        if args.once:
            manager.run_scraping_cycle()
        else:
            manager.start_monitoring()
            
    except KeyboardInterrupt:
        print("\nShutting down Homeus...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 