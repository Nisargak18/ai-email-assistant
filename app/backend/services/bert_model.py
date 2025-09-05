from __future__ import annotations

from functools import lru_cache
from typing import Tuple

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


@lru_cache(maxsize=1)
def get_bert_components():
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModel.from_pretrained("bert-base-uncased")
    return tokenizer, model


def _cls_embedding(text: str) -> np.ndarray:
    tokenizer, model = get_bert_components()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
    last_hidden = outputs.last_hidden_state
    cls_vec = last_hidden[:, 0, :].squeeze(0).cpu().numpy()
    return cls_vec


def analyze_with_bert(body: str) -> Tuple[str, str]:
    vec = _cls_embedding(body)

    positive_keywords = ["thank", "great", "good", "appreciate", "love", "happy"]
    negative_keywords = ["issue", "problem", "error", "fail", "bad", "angry"]

    text_lower = body.lower()
    pos_hits = sum(k in text_lower for k in positive_keywords)
    neg_hits = sum(k in text_lower for k in negative_keywords)

    if pos_hits > neg_hits:
        sentiment = "positive"
    elif neg_hits > pos_hits:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    urgent_indicators = [
        "urgent",
        "asap",
        "immediately",
        "critical",
        "priority",
        "severe",
        "down",
    ]
    is_urgent = any(k in text_lower for k in urgent_indicators)
    priority = "urgent" if is_urgent else "not_urgent"

    _ = float(vec.mean())  # Ensure model executed

    return sentiment, priority


