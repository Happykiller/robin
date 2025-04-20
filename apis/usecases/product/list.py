# apis\usecases\product\list.py
import logging
from typing import List, Optional

from services.i18n.translation import TranslationService
from interfaces.repositories.product import ProductRepository
from exposers.schemas.product import Product, ProductTranslation

logger = logging.getLogger(__name__)

def list_products(locale: str, repository: ProductRepository, translator: TranslationService) -> List[Product]:
    raw_products = repository.list(locale)
    
    raw_products_cleaned = [
        {
            "code": p["code"],
            "translation": p.get("translation"),
            "translations": p.get("translations", [])
        }
        for p in raw_products
    ]
    
    logger.info(f"[list_products] Requested locale: {locale}")
    logger.info(f"[list_products] Raw products: {raw_products_cleaned}")
    
    products = []

    for p in raw_products:
        # ⚠️ On récupère bien l'objet interne "translation"
        translation_entry = p["translation"]
        translation_data = None

        if translation_entry and "translation" in translation_entry:
            translation_data = translation_entry["translation"]
        else:
            # fallback via "en"
            en_translation = next(
                (t["translation"] for t in p["translations"] if t["locale"] == "en"),
                None
            )
            if en_translation and "title" in en_translation and "description" in en_translation:
                title = translator.translate(en_translation["title"], src="en", dest=locale)
                description = translator.translate(en_translation["description"], src="en", dest=locale)
                translation_data = {"title": title, "description": description}

        products.append(
            Product(
                code=p["code"],
                translation=build_safe_translation(translation_data)
            )
        )

    return products


def build_safe_translation(translation: Optional[dict]) -> Optional[ProductTranslation]:
    if translation and "title" in translation and "description" in translation:
        return ProductTranslation(
            title=translation["title"],
            description=translation["description"]
        )
    return None