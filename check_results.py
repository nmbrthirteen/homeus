#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.storage.database import Database

def check_results():
    db = Database('data/homeus.db')
    stats = db.get_stats()
    
    print('📊 Database Statistics:')
    print(f'  Total properties: {stats["total_properties"]}')
    print(f'  Today properties: {stats["today_properties"]}')
    print()
    
    recent = db.get_recent_properties(10)
    print('🏠 Recent Properties:')
    for i, prop in enumerate(recent[:8], 1):
        print(f'  {i}. {prop["title"][:60]}...')
        print(f'     💰 {prop["price"]} {prop["currency"]} | 📍 {prop["location"]}')
        print(f'     🆔 {prop["property_id"]} | 📅 {prop["scraped_at"]}')
        print()

if __name__ == "__main__":
    check_results() 