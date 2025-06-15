import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from pathlib import Path
import logging

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.property import Property

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    property_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    price INTEGER,
                    currency TEXT DEFAULT 'USD',
                    location TEXT,
                    district TEXT,
                    size REAL,
                    rooms INTEGER,
                    bedrooms INTEGER,
                    floor TEXT,
                    total_floors INTEGER,
                    property_type TEXT,
                    description TEXT,
                    images TEXT,
                    source_url TEXT NOT NULL,
                    detail_url TEXT,
                    listing_date DATETIME,
                    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    hash TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS scraping_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed_at DATETIME,
                    properties_found INTEGER DEFAULT 0,
                    new_properties INTEGER DEFAULT 0,
                    errors TEXT,
                    status TEXT DEFAULT 'running'
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_property_id ON properties(property_id)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_last_seen ON properties(last_seen)
            ''')
            
            conn.commit()
    
    def is_new_property(self, property_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT COUNT(*) FROM properties WHERE property_id = ?',
                (property_id,)
            )
            return cursor.fetchone()[0] == 0
    
    def save_property(self, property: Property) -> bool:
        try:
            data = property.to_dict()
            data['hash'] = property.generate_hash()
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO properties (
                        property_id, title, price, currency, location, district,
                        size, rooms, bedrooms, floor, total_floors, property_type,
                        description, images, source_url, detail_url, listing_date,
                        scraped_at, last_seen, is_active, hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['property_id'], data['title'], data['price'], data['currency'],
                    data['location'], data.get('district'), data.get('size'),
                    data.get('rooms'), data.get('bedrooms'), data.get('floor'),
                    data.get('total_floors'), data['property_type'], data.get('description'),
                    data['images'], data['source_url'], data.get('detail_url'),
                    data.get('listing_date'), data['scraped_at'], data['scraped_at'],
                    True, data['hash']
                ))
                conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error saving property {property.property_id}: {e}")
            return False
    
    def update_property_last_seen(self, property_id: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'UPDATE properties SET last_seen = CURRENT_TIMESTAMP WHERE property_id = ?',
                (property_id,)
            )
            conn.commit()
    
    def get_recent_properties(self, limit: int = 50) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM properties 
                ORDER BY scraped_at DESC 
                LIMIT ?
            ''', (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def start_scraping_session(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'INSERT INTO scraping_sessions (started_at, status) VALUES (CURRENT_TIMESTAMP, "running")'
            )
            conn.commit()
            return cursor.lastrowid
    
    def finish_scraping_session(self, session_id: int, properties_found: int, new_properties: int, errors: str = None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE scraping_sessions 
                SET completed_at = CURRENT_TIMESTAMP, 
                    properties_found = ?, 
                    new_properties = ?, 
                    errors = ?, 
                    status = "completed"
                WHERE id = ?
            ''', (properties_found, new_properties, errors, session_id))
            conn.commit()
    
    def get_stats(self) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM properties')
            total_properties = cursor.fetchone()[0]
            
            cursor = conn.execute('SELECT COUNT(*) FROM properties WHERE DATE(scraped_at) = DATE("now")')
            today_properties = cursor.fetchone()[0]
            
            cursor = conn.execute('SELECT COUNT(*) FROM scraping_sessions WHERE DATE(started_at) = DATE("now")')
            today_sessions = cursor.fetchone()[0]
            
            return {
                'total_properties': total_properties,
                'today_properties': today_properties,
                'today_sessions': today_sessions
            } 