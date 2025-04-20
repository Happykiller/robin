# apis\apis\resolvers\product.py
import strawberry
from typing import List, Optional

from usecases.product.search import search_products
from services.i18n.translation import TranslationService
from usecases.product import create, list as list_usecase
from exposers.schemas.product import Product, ProductInput
from interfaces.repositories.product import ProductRepository
from services.embeddings.labse_embedder import EmbeddingService

@strawberry.type
class ProductQuery:
    @strawberry.field
    def products(self, locale: str, limit: Optional[int] = None, info=None) -> List[Product]:
        repo: ProductRepository = info.context["repository"]
        translator: TranslationService = info.context["translator"]
        return list_usecase.list_products(locale, repo, translator, limit=limit)
    
    @strawberry.field
    def search_products(self, text: str, locale: str, limit: Optional[int] = None, info=None) -> List[Product]:
        repo = info.context["repository"]
        embedder = info.context["embedder"]
        translator = info.context["translator"]
        return search_products(text, locale, repo, translator, embedder, limit)

@strawberry.type
class ProductMutation:
    @strawberry.mutation
    def create_product(self, product: ProductInput, info) -> bool:
        repo: ProductRepository = info.context["repository"]
        embedder: EmbeddingService = info.context["embedder"]
        return create.create_product(product, repo, embedder)
