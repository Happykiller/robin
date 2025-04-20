# apis\usecases\product\list.py
import logging
from typing import List, Optional

from usecases.i18n.resolve import resolve_translation
from services.i18n.translation import TranslationService
from services.embeddings.labse_embedder import LANG_PRIORITY
from interfaces.repositories.product import ProductRepository
from exposers.schemas.product import Product, ProductTranslation

logger = logging.getLogger(__name__)

def list_products(locale: str, repository: ProductRepository, translator: TranslationService, limit: Optional[int] = None) -> List[Product]:
    raw_products = repository.list(locale)
    
    raw_products_cleaned = [
        {
            "code": p["code"],
            "translation": p.get("translation"),
            "translations": p.get("translations", [])
        }
        for p in raw_products
    ]
    
    logger.debug(f"[list_products] Requested locale: {locale}")
    logger.debug(f"[list_products] Raw products: {raw_products_cleaned}")
    
    products = []

    for p in raw_products:
        resolved = resolve_translation(p, locale, translator)
        products.append(Product(code=p["code"], translation=resolved))

    if limit:
            return products[:limit]
    return products


def build_safe_translation(translation: Optional[dict]) -> Optional[ProductTranslation]:
    if translation and "title" in translation and "description" in translation:
        return ProductTranslation(
            title=translation["title"],
            description=translation["description"]
        )
    return None