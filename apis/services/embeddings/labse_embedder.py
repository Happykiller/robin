# apis\services\embeddings\labse_embedder.py
import torch
from typing import List, Optional
from transformers import AutoTokenizer, AutoModel

LANG_PRIORITY = ["en", "fr", "es", "it"]

class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/LaBSE"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def encode_text(self, text: str) -> List[float]:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]  # CLS token
        return embeddings[0].tolist()

    def encode_field_by_lang_priority(self, translations: List[dict], field: str) -> Optional[List[float]]:
        translations_map = {t["locale"]: t["translation"] for t in translations}
        for lang in LANG_PRIORITY:
            if lang in translations_map and field in translations_map[lang]:
                return self.encode_text(translations_map[lang][field])
        return None
