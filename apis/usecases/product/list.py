# apis\usecases\product\list.py
from typing import List

from interfaces.repositories.product import ProductRepository
from services.embeddings.labse_embedder import EmbeddingService
from exposers.schemas.product import Product, ProductTranslation

def list_products(locale: str, repository: ProductRepository, embedder: EmbeddingService) -> List[Product]:
    raw_products = repository.list(locale)

    result = []

    for p in raw_products:
        trans_entry = p.get("translation") or {}
        inner_trans = trans_entry.get("translation") or {}

        title = inner_trans.get("title")
        description = inner_trans.get("description")

        result.append(Product(
            code=p["code"],
            translation=ProductTranslation(title=title, description=description)
            if title and description else None
        ))

    return result
