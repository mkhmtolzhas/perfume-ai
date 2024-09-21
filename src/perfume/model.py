from pydantic import BaseModel
from typing import Optional, List, Dict

class PerfumeInDB(BaseModel):
    id: Optional[str] = None
    name: str
    brand: str
    type: str
    price: int
    description: str
    attributes: list
    image: list
    url: str


    def to_bson(self):
        return {
            'name': self.name,
            'brand': self.brand,
            'type': self.type,
            'price': self.price,
            'description': self.description,
            'attributes': self.attributes,
            'image': self.image,
            'url': self.url
        }