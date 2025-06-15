#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.storage.database import Database
from src.storage.sheets_manager import SheetsManager
from src.models.property import Property
from src.utils.config import load_config
import json
from datetime import datetime

def reset_and_export():
    print("🔄 Resetting Google Sheet and re-exporting data...")
    
    config = load_config('config/config.yaml')
    
    if not config['google_sheets']['enabled']:
        print("❌ Google Sheets is not enabled in config")
        return
    
    db = Database('data/homeus.db')
    sheets = SheetsManager(config['google_sheets'])
    
    if not sheets.worksheet:
        print("❌ Could not connect to Google Sheets")
        return
    
    print("✅ Connected to Google Sheets")
    
    sheets._setup_headers()
    print("✅ Headers set up")
    
    recent_properties = db.get_recent_properties(50)
    print(f"📊 Found {len(recent_properties)} properties to export")
    
    properties_to_export = []
    for prop_data in recent_properties:
        try:
            images_list = json.loads(prop_data['images']) if prop_data['images'] else []
            
            prop = Property(
                property_id=prop_data['property_id'],
                title=prop_data['title'],
                price=prop_data['price'],
                currency=prop_data['currency'],
                location=prop_data['location'],
                district=prop_data['district'],
                size=prop_data['size'],
                rooms=prop_data['rooms'],
                bedrooms=prop_data['bedrooms'],
                floor=prop_data['floor'],
                total_floors=prop_data['total_floors'],
                property_type=prop_data['property_type'],
                description=prop_data['description'],
                images=images_list,
                source_url=prop_data['source_url'],
                detail_url=prop_data['detail_url'],
                listing_date=datetime.fromisoformat(prop_data['listing_date']) if prop_data['listing_date'] else None,
                scraped_at=datetime.fromisoformat(prop_data['scraped_at'])
            )
            properties_to_export.append(prop)
        except Exception as e:
            print(f"⚠️ Error processing property {prop_data['property_id']}: {e}")
            continue
    
    if properties_to_export:
        success = sheets.add_properties_batch(properties_to_export)
        if success:
            print(f"✅ Successfully exported {len(properties_to_export)} properties to Google Sheets")
            print(f"🔗 View your sheet: {sheets.get_sheet_url()}")
        else:
            print("❌ Failed to export properties to Google Sheets")
    else:
        print("⚠️ No properties to export")

if __name__ == "__main__":
    reset_and_export() 