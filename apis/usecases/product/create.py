# apis\usecases\product\create.py
from domains.product import ProductInternal
from exposers.schemas.product import ProductInput
from interfaces.repositories.product import ProductRepository
from services.embeddings.labse_embedder import EmbeddingService

def create_product(
    product: ProductInput,
    repository: ProductRepository,
    embedder: EmbeddingService
) -> bool:
    # Embedding des champs multilingues
    raw_translations = [
        { "locale": t.locale, "translation": { "title": t.translation.title, "description": t.translation.description } }
        for t in product.translations
    ]

    emb_title = embedder.encode_field_by_lang_priority(raw_translations, "title")
    emb_desc = embedder.encode_field_by_lang_priority(raw_translations, "description")

    internal_product = ProductInternal(
        code=product.code,
        translations=raw_translations,
        embedding_title=emb_title,
        embedding_description=emb_desc,
    )

    return repository.save(internal_product)
