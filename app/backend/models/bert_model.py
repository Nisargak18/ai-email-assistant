from __future__ import annotations

from functools import lru_cache
from typing import Literal, Tuple

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


class BertClassifier:
    """Lightweight classifier using BERT embeddings + heuristics.

    Loads tokenizer and model once and reuses them for all predictions.
    Returns sentiment (positive/negative/neutral) and priority (urgent/not_urgent).
    """

    positive_keywords = ["thank", "great", "good", "appreciate", "love", "happy"]
    negative_keywords = ["issue", "problem", "error", "fail", "bad", "angry", "frustrated", "frustration"]
    urgent_indicators = ["urgent", "asap", "immediately", "critical", "priority", "severe", "down"]

    def __init__(self, model_name: str = "bert-base-uncased") -> None:
        self.model_name = model_name
        self.tokenizer, self.model = self._get_components()

    @lru_cache(maxsize=1)
    def _get_components(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModel.from_pretrained(self.model_name)
        return tokenizer, model

    def _cls_embedding(self, text: str) -> np.ndarray:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
        with torch.no_grad():
            outputs = self.model(**inputs)
        last_hidden = outputs.last_hidden_state
        cls_vec = last_hidden[:, 0, :].squeeze(0).cpu().numpy()
        return cls_vec

    def predict(self, body: str) -> Tuple[Literal["positive", "negative", "neutral"], Literal["urgent", "not_urgent"]]:
        vec = self._cls_embedding(body)

        text_lower = body.lower()
        pos_hits = sum(k in text_lower for k in self.positive_keywords)
        neg_hits = sum(k in text_lower for k in self.negative_keywords)

        if pos_hits > neg_hits:
            sentiment: Literal["positive", "negative", "neutral"] = "positive"
        elif neg_hits > pos_hits:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        is_urgent = any(k in text_lower for k in self.urgent_indicators)
        priority: Literal["urgent", "not_urgent"] = "urgent" if is_urgent else "not_urgent"

        _ = float(vec.mean())  # ensure model executed
        return sentiment, priority


