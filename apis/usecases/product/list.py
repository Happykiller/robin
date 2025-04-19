# apis\usecases\product\list.py
from typing import List
from apis.schemas.product import Product, ProductTranslation
from interfaces.repositories.product_repository import ProductRepository

def list_products(locale: str, repository: ProductRepository) -> List[Product]:
    raw_products = repository.list(locale)
    return [
        Product(
            code=p["code"],
            translation=ProductTranslation(
                title=p["translation"].title,
                description=p["translation"].description
            ) if p["translation"] else None
        )
        for p in raw_products
    ]
