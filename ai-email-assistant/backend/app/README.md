# FastAPI Email Assistant

This project is a FastAPI application designed to assist with email processing using machine learning models from Hugging Face. It includes features for sentiment analysis and priority classification using a BERT model, as well as generating context-aware replies using a T5 model.

## Project Structure

```
ai-email-assistant
├── backend
│   └── app
│       ├── main.py                # Entry point of the FastAPI application
│       ├── api
│       │   ├── __init__.py        # Initializes the API package
│       │   └── email_router.py     # Defines email-related API routes
│       ├── models
│       │   ├── __init__.py        # Initializes the models package
│       │   ├── bert_model.py       # BERT model for sentiment and priority classification
│       │   └── t5_model.py         # T5 model for generating replies
│       ├── services
│       │   ├── __init__.py        # Initializes the services package
│       │   ├── email_processing.py  # Helper functions for email processing
│       │   └── response_generation.py # Functions for generating responses
│       ├── utils
│       │   ├── __init__.py        # Initializes the utils package
│       │   └── bert_loader.py      # Utility functions for loading the BERT model
│       └── README.md               # Documentation for the FastAPI application
└── README.md                       # Main documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd ai-email-assistant
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install fastapi[all] transformers pandas
   ```

4. **Run the application:**
   ```
   uvicorn backend.app.main:app --reload
   ```

## API Endpoints

- **GET /emails**: Fetches and returns filtered emails from a mock CSV file.
- **POST /analyze**: Accepts an email body and uses the BERT model to classify sentiment and urgency.
- **POST /respond**: Accepts an email subject and body, generating a context-aware reply using the T5 model.

## Usage Examples

### Fetch Emails
```
GET /emails?keywords=urgent
```

### Analyze Email
```
POST /analyze
{
  "text": "I need help with my account."
}
```

### Generate Reply
```
POST /respond
{
  "subject": "Account Assistance",
  "body": "I need help with my account."
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.