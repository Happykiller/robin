# apis\apis\schemas\product.py
import strawberry
from typing import List, Optional

@strawberry.type
class ProductTranslation:
    title: str
    description: str

@strawberry.type
class Product:
    code: str
    translation: Optional[ProductTranslation]

@strawberry.input
class ProductTranslationInput:
    title: str
    description: str

@strawberry.input
class TranslationEntryInput:
    locale: str
    translation: ProductTranslationInput

@strawberry.input
class ProductInput:
    code: str
    translations: List[TranslationEntryInput]
