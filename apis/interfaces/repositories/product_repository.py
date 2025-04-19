# apis\interfaces\repositories\product_repository.py
from abc import ABC, abstractmethod
from typing import List, Dict
from apis.schemas.product import ProductInput, ProductTranslationInput

class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: ProductInput) -> bool:
        pass

    @abstractmethod
    def list(self, locale: str) -> List[Dict]:
        pass
