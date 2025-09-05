from transformers import BertTokenizer, BertForSequenceClassification
import torch

class BertLoader:
    def __init__(self):
        self.model_name = 'bert-base-uncased'
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForSequenceClassification.from_pretrained(self.model_name)

    def load_model(self):
        return self.model

    def load_tokenizer(self):
        return self.tokenizer

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        return probabilities.argmax(dim=1).item(), probabilities.tolist()