# apis\domains\product.py
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ProductInternal:
    code: str
    translations: List[Dict]  # raw { locale, title, description }
    embedding_title: Optional[List[float]] = None
    embedding_description: Optional[List[float]] = None
