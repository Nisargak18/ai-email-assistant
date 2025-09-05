from __future__ import annotations

from functools import lru_cache
from typing import Optional

from transformers import T5ForConditionalGeneration, T5Tokenizer


class T5Responder:
    """Generates professional, empathetic replies using T5.

    Loads tokenizer and model once and reuses them.
    """

    def __init__(self, model_name: str = "t5-small") -> None:
        self.model_name = model_name
        self.tokenizer, self.model = self._get_components()

    @lru_cache(maxsize=1)
    def _get_components(self):
        tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        return tokenizer, model

    def respond(self, subject: str, body: str, sentiment: Optional[str] = None) -> str:
        empathy_prefix = ""
        if sentiment == "negative":
            empathy_prefix = (
                "I’m sorry for the trouble you’ve experienced. "
                "I understand how frustrating this can be. "
            )
        elif sentiment == "neutral":
            empathy_prefix = "Thanks for reaching out. "
        elif sentiment == "positive":
            empathy_prefix = "Thanks for the kind words. "

        instruction = (
            "You are a helpful support agent. Write a concise, professional reply "
            "addressing the user's concern. Maintain a polite tone, acknowledge the "
            "context, and offer clear next steps."
        )

        content = f"Subject: {subject}\nEmail: {body}\nReply should start with: {empathy_prefix}"

        input_text = f"summarize: {instruction}\n{content}"
        input_ids = self.tokenizer.encode(
            input_text, return_tensors="pt", truncation=True, max_length=512
        )

        outputs = self.model.generate(
            input_ids=input_ids,
            max_new_tokens=180,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            num_return_sequences=1,
            early_stopping=True,
        )
        reply = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return reply.strip()


