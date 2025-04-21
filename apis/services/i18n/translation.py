from typing import Dict, Tuple
from transformers import MarianMTModel, MarianTokenizer

class TranslationService:
    def __init__(self):
        self.models: Dict[Tuple[str, str], Tuple[MarianTokenizer, MarianMTModel]] = {}
        self.model_map = self.build_model_map()

    def build_model_map(self) -> Dict[Tuple[str, str], str]:
        return {
            ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
            ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
            ("en", "es"): "Helsinki-NLP/opus-mt-en-es",
            ("es", "en"): "Helsinki-NLP/opus-mt-es-en",
            ("en", "it"): "Helsinki-NLP/opus-mt-en-it",
            ("it", "en"): "Helsinki-NLP/opus-mt-it-en",
            ("fr", "es"): "Helsinki-NLP/opus-mt-fr-es",
            ("es", "fr"): "Helsinki-NLP/opus-mt-es-fr",
            ("es", "it"): "Helsinki-NLP/opus-mt-es-it",
            ("it", "es"): "Helsinki-NLP/opus-mt-it-es",
            ("it", "fr"): "Helsinki-NLP/opus-mt-it-fr",
        }

    def get_model_name(self, src: str, dest: str) -> str:
        key = (src, dest)
        if key in self.model_map:
            return self.model_map[key]
        elif (dest, src) in self.model_map:
            return None  # fallback logique, non via modèle direct
        else:
            raise ValueError(f"No MarianMT model or fallback available for: {src} → {dest}")

    def load_model(self, src: str, dest: str):
        key = (src, dest)
        if key not in self.models:
            model_name = self.get_model_name(src, dest)
            if model_name is None:
                return  # handled via inversion fallback
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)
            self.models[key] = (tokenizer, model)

    def translate(self, text: str, src: str = "en", dest: str = "fr") -> str:
        direct_key = (src, dest)

        # Cas 1 : modèle direct
        if direct_key in self.model_map:
            self.load_model(src, dest)
            tokenizer, model = self.models[direct_key]
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            translated = model.generate(**inputs)
            return tokenizer.decode(translated[0], skip_special_tokens=True)

        # Cas 2 : fallback par inversion si modèle inverse existe
        inverse_key = (dest, src)
        if inverse_key in self.model_map:
            print(f"[TranslationService] Fallback translation via {dest} → {src} (inversion)")

            self.load_model(dest, src)
            tokenizer, model = self.models[inverse_key]
            # Étape 1 : traduire de src vers dest via modèle inverse
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            translated = model.generate(**inputs)
            intermediate = tokenizer.decode(translated[0], skip_special_tokens=True)

            # Étape 2 : retraduire dans la direction souhaitée
            self.load_model(src, dest)
            tokenizer, model = self.models[inverse_key]  # on réutilise inverse ici par simplicité
            inputs = tokenizer(intermediate, return_tensors="pt", padding=True, truncation=True)
            translated = model.generate(**inputs)
            return tokenizer.decode(translated[0], skip_special_tokens=True)

        raise ValueError(f"Unable to translate from {src} to {dest}: no model or fallback available.")
