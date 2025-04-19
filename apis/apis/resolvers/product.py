# apis\apis\resolvers\product.py
import strawberry
from typing import List

from apis.schemas.product import Product, ProductInput, ProductTranslation
from interfaces.repositories.product_repository import ProductRepository
from usecases.product import create, list as list_usecase


@strawberry.type
class ProductQuery:
    @strawberry.field
    def products(self, locale: str, info) -> List[Product]:
        repo: ProductRepository = info.context["repository"]
        return list_usecase.list_products(locale, repo)


@strawberry.type
class ProductMutation:
    @strawberry.mutation
    def create_product(self, product: ProductInput, info) -> bool:
        repo: ProductRepository = info.context["repository"]
        return create.create_product(product, repo)
