# AI Email Assistant

This project is a FastAPI application designed to assist with email processing using machine learning models. It leverages Hugging Face's BERT and T5 models for sentiment analysis, urgency classification, and generating context-aware replies.

## Project Structure

```
ai-email-assistant
├── backend
│   └── app
│       ├── main.py                # Entry point of the FastAPI application
│       ├── api
│       │   ├── __init__.py        # Initialization for the API module
│       │   └── email_router.py     # FastAPI router for email-related APIs
│       ├── models
│       │   ├── __init__.py        # Initialization for the models module
│       │   ├── bert_model.py       # BERT model for sentiment and priority classification
│       │   └── t5_model.py         # T5 model for generating email replies
│       ├── services
│       │   ├── __init__.py        # Initialization for the services module
│       │   ├── email_processing.py  # Functions for processing emails
│       │   └── response_generation.py # Functions for generating responses
│       ├── utils
│       │   ├── __init__.py        # Initialization for the utils module
│       │   └── bert_loader.py      # Utility functions for loading the BERT model
│       └── README.md               # Documentation for the FastAPI application
└── README.md                       # Main documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd ai-email-assistant
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```
   uvicorn backend.app.main:app --reload
   ```

## API Endpoints

- **GET /emails**: Fetches and returns filtered emails from a mock CSV file.
- **POST /analyze**: Accepts an email body and uses the BERT model to classify sentiment and urgency.
- **POST /respond**: Accepts an email subject and body, generating a context-aware reply using the T5 model.

## Usage Examples

- To analyze an email:
  ```
  POST /analyze
  {
      "text": "I need help with my order."
  }
  ```

- To generate a reply:
  ```
  POST /respond
  {
      "subject": "Order Inquiry",
      "body": "I need help with my order."
  }
  ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.