from transformers import T5Tokenizer, T5ForConditionalGeneration

class T5Responder:
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("t5-small")
        self.model = T5ForConditionalGeneration.from_pretrained("t5-small")

    def generate_reply(self, subject: str, body: str) -> str:
        input_text = f"subject: {subject} context: {body}"
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        output = self.model.generate(input_ids)
        reply = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return reply