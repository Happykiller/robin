# apis\usecases\product\create.py
from apis.schemas.product import ProductInput
from interfaces.repositories.product_repository import ProductRepository

def create_product(product: ProductInput, repository: ProductRepository) -> bool:
    return repository.save(product)