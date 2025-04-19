# apis\services\db\memory.py
from typing import Dict, List, Optional
from apis.schemas.product import ProductInput, ProductTranslationInput
from apis.schemas.product import TranslationEntryInput
from interfaces.repositories.product_repository import ProductRepository

class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products: Dict[str, ProductInput] = {}

    def save(self, product: ProductInput) -> bool:
        if product.code in self.products:
            return False
        self.products[product.code] = product
        return True

    def list(self, locale: str) -> List[Dict]:
        results = []
        for product in self.products.values():
            translation: Optional[ProductTranslationInput] = None
            for entry in product.translations:
                if entry.locale == locale:
                    translation = entry.translation
                    break

            results.append({
                "code": product.code,
                "translation": translation
            })
        return results
