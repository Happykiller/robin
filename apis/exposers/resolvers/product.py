# apis\apis\resolvers\product.py
import strawberry
from typing import List

from usecases.product import create, list as list_usecase
from exposers.schemas.product import Product, ProductInput
from interfaces.repositories.product import ProductRepository
from services.embeddings.labse_embedder import EmbeddingService

@strawberry.type
class ProductQuery:
    @strawberry.field
    def products(self, locale: str, info) -> List[Product]:
        repo: ProductRepository = info.context["repository"]
        embedder: EmbeddingService = info.context["embedder"]
        return list_usecase.list_products(locale, repo, embedder)

@strawberry.type
class ProductMutation:
    @strawberry.mutation
    def create_product(self, product: ProductInput, info) -> bool:
        repo: ProductRepository = info.context["repository"]
        embedder: EmbeddingService = info.context["embedder"]
        return create.create_product(product, repo, embedder)
