# apis\usecases\product\create.py
from domains.product import ProductInternal
from exposers.schemas.product import ProductInput
from services.i18n.translation import TranslationService
from interfaces.repositories.product import ProductRepository
from services.embeddings.labse_embedder import EmbeddingService, LANG_PRIORITY

def create_product(
    product: ProductInput,
    repository: ProductRepository,
    embedder: EmbeddingService,
    translator: TranslationService
) -> bool:
    # 1. Récupération des traductions utilisateur
    user_translations = [
        { "locale": t.locale, "translation": { "title": t.translation.title, "description": t.translation.description } }
        for t in product.translations
    ]
    translations_map = {t["locale"]: t["translation"] for t in user_translations}

    # 2. Encodage à partir des champs utilisateurs (embedding uniquement)
    emb_title = embedder.encode_field_by_lang_priority(user_translations, "title")
    emb_desc = embedder.encode_field_by_lang_priority(user_translations, "description")

    # 3. Détermination de la langue source pour fallback
    source_lang = next((lang for lang in LANG_PRIORITY if lang in translations_map), None)
    if source_lang is None:
        return False

    source = translations_map[source_lang]

    # 4. Compléter les langues manquantes avec traductions automatiques
    for lang in LANG_PRIORITY:
        if lang not in translations_map:
            translated_title = translator.translate(source["title"], src=source_lang, dest=lang)
            translated_desc = translator.translate(source["description"], src=source_lang, dest=lang)
            translations_map[lang] = {
                "title": translated_title,
                "description": translated_desc
            }

    # 5. Reconstruction normalisée
    raw_translations = [
        { "locale": locale, "translation": trans }
        for locale, trans in translations_map.items()
    ]

    internal_product = ProductInternal(
        code=product.code,
        translations=raw_translations,
        embedding_title=emb_title,
        embedding_description=emb_desc,
    )

    return repository.save(internal_product)
