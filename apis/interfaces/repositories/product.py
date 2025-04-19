# interfaces/repositories/product.py
from typing import List, Dict
from abc import ABC, abstractmethod

from domains.product import ProductInternal

class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: ProductInternal) -> bool:
        pass

    @abstractmethod
    def list(self, locale: str) -> List[Dict]:
        pass
