import pandas as pd
from typing import List, Tuple

from .t5_model import generate_with_t5  # Use relative import if same folder, adjust if needed

CSV_DEFAULT_PATH = "backend/app/sample_support_Emails_Dataset.csv"
KEYWORDS = ["support", "request", "help"]

def load_emails(csv_path: str = CSV_DEFAULT_PATH) -> List[dict]:
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]
    for col in ["sender", "subject", "body", "date"]:
        if col not in df.columns:
            raise ValueError(f"CSV missing required column: {col}")
    mask = df["subject"].astype(str).str.lower().str.contains("|".join(KEYWORDS), na=False)
    filtered = df.loc[mask, ["sender", "subject", "body", "date"]]
    return filtered.to_dict(orient="records")

def analyze_email(text: str) -> Tuple[str, str]:
    # Optional: add your own ML logic here
    pass

def generate_reply(subject: str, body: str) -> str:
    return generate_with_t5(subject, body)