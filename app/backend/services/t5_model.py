from functools import lru_cache
from transformers import T5ForConditionalGeneration, T5Tokenizer

@lru_cache(maxsize=1)
def get_t5_components():
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    return tokenizer, model

def generate_with_t5(subject: str, body: str) -> str:
    tokenizer, model = get_t5_components()
    prompt = (
        "You are a helpful support agent. Write a concise, professional reply "
        "addressing the user's concern. Maintain a polite tone, acknowledge the "
        "issue, and offer next steps.\n"
        f"\nSubject: {subject}\nEmail: {body}"
    )
    input_ids = tokenizer.encode(
        f"summarize: {prompt}",
        return_tensors="pt",
        truncation=True,
        max_length=512
    )
    outputs = model.generate(
        input_ids,
        max_new_tokens=100,
        top_p=0.7,
        do_sample=True,
        num_return_sequences=1,
        early_stopping=True
    )
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply.strip()