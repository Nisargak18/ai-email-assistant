from __future__ import annotations

from backend.models.bert_model import BertClassifier


def main() -> None:
    clf = BertClassifier()
    sample = (
        "Hello team, I'm facing an issue with my account login. "
        "This is urgent and needs immediate attention."
    )
    sentiment, priority = clf.predict(sample)
    print({"sentiment": sentiment, "priority": priority})


if __name__ == "__main__":
    main()
sender,subject,body,date
alice@example.com,Support: Unable to login,"Hi team, I'm facing an issue logging into my account. It says password incorrect even after reset. Please help ASAP.",2024-08-12
bob@example.com,Request: Feature inquiry,"Hello, I'd love to know if you plan to add dark mode. Thanks for the great product!",2024-08-15
carol@example.com,Query about billing,"My invoice shows an extra charge this month. This is urgent and needs immediate attention.",2024-08-20
dave@example.com,Help setting up account,"Could you guide me through setting up my account? Appreciate your support.",2024-08-25

