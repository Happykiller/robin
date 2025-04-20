# apis\services\i18n\translationService.py
from typing import Dict, Tuple
from transformers import MarianMTModel, MarianTokenizer

class TranslationService:
    def __init__(self):
        self.models: Dict[Tuple[str, str], Tuple[MarianTokenizer, MarianMTModel]] = {}

    def load_model(self, src: str, dest: str):
        key = (src, dest)
        if key not in self.models:
            model_name = f"Helsinki-NLP/opus-mt-{src}-{dest}"
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)
            self.models[key] = (tokenizer, model)

    def translate(self, text: str, src: str = "en", dest: str = "fr") -> str:
        self.load_model(src, dest)
        tokenizer, model = self.models[(src, dest)]
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        return tokenizer.decode(translated[0], skip_special_tokens=True)

