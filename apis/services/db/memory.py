# apis\services\db\memory.py
from typing import Dict, List

from domains.product import ProductInternal
from interfaces.repositories.product import ProductRepository

class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products: Dict[str, ProductInternal] = {}

    def save(self, product: ProductInternal) -> bool:
        if product.code in self.products:
            return False
        self.products[product.code] = product
        return True

    def list(self, locale: str) -> List[Dict]:
        results = []
        for product in self.products.values():
            translation = next(
                (t for t in product.translations if t["locale"] == locale),
                None
            )
            results.append({
                "code": product.code,
                "translation": translation,
                "translations": product.translations,
                "embedding_title": product.embedding_title,
                "embedding_description": product.embedding_description,
            })
        return results
