# apis\usecases\i18n\resolve.py
import logging
from typing import Optional, Dict

from exposers.schemas.product import ProductTranslation
from services.i18n.translation import TranslationService
from services.embeddings.labse_embedder import LANG_PRIORITY

logger = logging.getLogger(__name__)

def resolve_translation(product: Dict, locale: str, translator: TranslationService) -> Optional[ProductTranslation]:
    translation_entry = product.get("translation")
    translation_data = None

    if translation_entry and "translation" in translation_entry:
        translation_data = translation_entry["translation"]
    else:
        available = {t["locale"]: t["translation"] for t in product.get("translations", [])}
        source_lang = next((lang for lang in LANG_PRIORITY if lang in available), None)

        if source_lang:
            source = available[source_lang]
            title = translator.translate(source["title"], src=source_lang, dest=locale)
            description = translator.translate(source["description"], src=source_lang, dest=locale)
            translation_data = {"title": title, "description": description}
            logger.debug(f"[resolve_translation] Fallback translation from '{source_lang}' to '{locale}'")

    if translation_data and "title" in translation_data and "description" in translation_data:
        return ProductTranslation(
            title=translation_data["title"],
            description=translation_data["description"]
        )

    return None
