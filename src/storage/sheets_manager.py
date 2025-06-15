import gspread
from google.auth.exceptions import GoogleAuthError
import logging
from typing import List, Optional
from datetime import datetime
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.property import Property

class SheetsManager:
    def __init__(self, config: dict):
        self.config = config
        self.client = None
        self.worksheet = None
        self._init_sheets()
    
    def _init_sheets(self):
        if not self.config.get('enabled', False):
            return
        
        try:
            if self.config.get('service_account_file'):
                self.client = gspread.service_account(filename=self.config['service_account_file'])
            else:
                logging.warning("Google Sheets service account file not configured")
                return
            
            sheet = self.client.open_by_key(self.config['sheet_id'])
            
            try:
                self.worksheet = sheet.worksheet(self.config['worksheet_name'])
            except gspread.WorksheetNotFound:
                self.worksheet = sheet.add_worksheet(
                    title=self.config['worksheet_name'],
                    rows=1000,
                    cols=20
                )
                self._setup_headers()
            
            logging.info("Google Sheets integration initialized successfully")
            
        except GoogleAuthError as e:
            logging.error(f"Google Sheets authentication failed: {e}")
        except Exception as e:
            logging.error(f"Google Sheets initialization failed: {e}")
    
    def _setup_headers(self):
        if not self.worksheet:
            return
        
        headers = [
            'Property ID', 'Title', 'Price', 'Currency', 'Location', 'District',
            'Size (m²)', 'Rooms', 'Bedrooms', 'Floor', 'Total Floors',
            'Property Type', 'Description', 'Images Count', 'Source URL',
            'Detail URL', 'Listing Date', 'Scraped At', 'Status'
        ]
        
        try:
            self.worksheet.clear()
            self.worksheet.update('A1:S1', [headers])
            self.worksheet.format('A1:S1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            logging.info("Google Sheets headers set up successfully")
        except Exception as e:
            logging.error(f"Error setting up Google Sheets headers: {e}")
    
    def add_property(self, property: Property) -> bool:
        if not self.worksheet:
            return False
        
        try:
            row_data = [
                property.property_id,
                property.title,
                property.price or '',
                property.currency,
                property.location,
                property.district or '',
                f"{property.size} m²" if property.size else '',
                property.rooms or '',
                property.bedrooms or '',
                property.floor or '',
                property.total_floors or '',
                property.property_type,
                (property.description[:100] + '...') if property.description and len(property.description) > 100 else (property.description or ''),
                len(property.images),
                property.source_url,
                property.detail_url or '',
                property.listing_date.strftime('%Y-%m-%d %H:%M:%S') if property.listing_date else '',
                property.scraped_at.strftime('%Y-%m-%d %H:%M:%S'),
                'NEW'
            ]
            
            self.worksheet.append_row(row_data)
            logging.info(f"Added property to Google Sheets: {property.property_id}")
            return True
            
        except Exception as e:
            logging.error(f"Error adding property to Google Sheets: {e}")
            return False
    
    def add_properties_batch(self, properties: List[Property]) -> bool:
        if not self.worksheet or not properties:
            return False
        
        try:
            rows_data = []
            for property in properties:
                row_data = [
                    property.property_id,
                    property.title,
                    property.price or '',
                    property.currency,
                    property.location,
                    property.district or '',
                    f"{property.size} m²" if property.size else '',
                    property.rooms or '',
                    property.bedrooms or '',
                    property.floor or '',
                    property.total_floors or '',
                    property.property_type,
                    (property.description[:100] + '...') if property.description and len(property.description) > 100 else (property.description or ''),
                    len(property.images),
                    property.source_url,
                    property.detail_url or '',
                    property.listing_date.strftime('%Y-%m-%d %H:%M:%S') if property.listing_date else '',
                    property.scraped_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'NEW'
                ]
                rows_data.append(row_data)
            
            self.worksheet.append_rows(rows_data)
            logging.info(f"Added {len(properties)} properties to Google Sheets")
            return True
            
        except Exception as e:
            logging.error(f"Error adding properties batch to Google Sheets: {e}")
            return False
    
    def update_property_status(self, property_id: str, status: str) -> bool:
        if not self.worksheet:
            return False
        
        try:
            cell = self.worksheet.find(property_id)
            if cell:
                self.worksheet.update_cell(cell.row, 19, status)  # Status column
                return True
        except Exception as e:
            logging.error(f"Error updating property status in Google Sheets: {e}")
        
        return False
    
    def get_sheet_url(self) -> Optional[str]:
        if not self.config.get('sheet_id'):
            return None
        return f"https://docs.google.com/spreadsheets/d/{self.config['sheet_id']}" 