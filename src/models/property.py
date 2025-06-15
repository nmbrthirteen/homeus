from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import hashlib
import json

class Property(BaseModel):
    property_id: str
    title: str
    price: Optional[int] = None
    currency: str = "USD"
    location: str
    district: Optional[str] = None
    size: Optional[float] = None
    rooms: Optional[int] = None
    bedrooms: Optional[int] = None
    floor: Optional[str] = None
    total_floors: Optional[int] = None
    property_type: str
    description: Optional[str] = None
    images: List[str] = Field(default_factory=list)
    source_url: str
    detail_url: Optional[str] = None
    listing_date: Optional[datetime] = None
    scraped_at: datetime = Field(default_factory=datetime.now)
    is_new: bool = True
    
    def generate_hash(self) -> str:
        content = f"{self.title}{self.price}{self.location}{self.size}{self.rooms}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def to_dict(self) -> dict:
        data = self.model_dump()
        data['images'] = json.dumps(self.images)
        data['scraped_at'] = self.scraped_at.isoformat()
        if self.listing_date:
            data['listing_date'] = self.listing_date.isoformat()
        return data 