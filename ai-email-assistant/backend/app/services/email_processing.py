def load_emails(csv_path):
    import pandas as pd

    df = pd.read_csv(csv_path)
    # Filter emails based on specified keywords
    filtered_emails = df[df['subject'].str.contains('urgent|important', case=False)]
    return filtered_emails.to_dict(orient='records')

def analyze_email(text):
    from ..models.bert_model import BertClassifier

    classifier = BertClassifier()
    sentiment, priority = classifier.classify(text)
    return {
        "sentiment": sentiment,
        "priority": priority
    }

def generate_reply(subject, body):
    from ..models.t5_model import T5Responder

    responder = T5Responder()
    reply = responder.generate_reply(subject, body)
    return reply