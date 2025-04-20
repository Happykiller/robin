# apis\usecases\product\search.py
import logging
from typing import List, Optional, Tuple

from exposers.schemas.product import Product
from usecases.i18n.resolve import resolve_translation
from services.i18n.translation import TranslationService
from services.embeddings.similarity import cosine_similarity
from interfaces.repositories.product import ProductRepository
from services.embeddings.labse_embedder import EmbeddingService

logger = logging.getLogger(__name__)

SIMILARITY_THRESHOLD = 0.65

def search_products(
    text: str,
    locale: str,
    repository: ProductRepository,
    translator: TranslationService,
    embedder: EmbeddingService,
    limit: Optional[int] = None
) -> List[Product]:
    query_vector = embedder.encode_text(text)
    raw_products = repository.list(locale)
    
    def filter_and_score(products: List[dict], embedding_key: str) -> List[Tuple[float, dict]]:
        scored = []
        for p in products:
            embedding = p.get(embedding_key)
            if embedding:
                score = cosine_similarity(query_vector, embedding)
                if score >= SIMILARITY_THRESHOLD:
                    scored.append((score, p))
        return sorted(scored, key=lambda x: x[0], reverse=True)

    # Recherche sur les titres
    matches = filter_and_score(raw_products, "embedding_title")

    # Si rien trouvé, on tente sur la description
    if not matches:
        matches = filter_and_score(raw_products, "embedding_description")

    results = []
    for score, p in matches[:limit]:
        resolved = resolve_translation(p, locale, translator)
        results.append(Product(code=p["code"], translation=resolved, score=score))

    logger.debug(f"[search_products] query='{text}' locale={locale} results={len(results)}")
    return results
