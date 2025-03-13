# Customer Support Insights API

This project is a backend service built with FastAPI that analyzes Twitter customer support data and provides actionable insights for companies.

## Features

- **Data Ingestion**: Load tweet dataset via a CSV file.
- **Company Insights**: Retrieve metrics such as response rate, conversation ratio, and average response time.
- **AI-Enhanced Insights**: Analyze customer tweets using a simulated Hugging Face model to extract common issues.
- **Security**: JWT-based authentication.
- **Logging**: HTTP request and key backend event logging.
- **Dockerized**: Easily deployable via Docker and docker-compose.

## Setup Instructions

1. **Clone the repository**

```
git clone <repository_url>
cd jelou-python-test
```
2. **Docker**

To run the application in Docker:

```
docker-compose up --build
```

## API Endpoints

* POST /ingest: Upload a CSV file to load the tweet dataset.
* GET /companies/{company_id}/insights: Get aggregated metrics for a company.
* GET /companies/{company_id}/ai-insights: Get AI-enhanced insights on common customer issues.

## Security
JWT-based authentication is implemented. Include the token in the Authorization header as `Bearer <token>`.

## Logging
HTTP requests and key backend events are logged using Python’s logging module.

## Project Structure

```
CustomerSupportInsightsAPI/
├── app/                # Application code
│   ├── main.py         # Entry point for FastAPI
│   ├── config.py       # Configuration settings
│   ├── models.py       # Data models (Pydantic)
│   ├── database.py     # In-memory data storage (pandas)
│   ├── dependencis.py  # helper for jwt security
│   ├── logger.py       # helper for logging incomming http request
│   ├── routers/        # API routes for ingestion and insights
│   └── services/       # Business logic and AI integration
├── tests/              # Unit and integration tests
├── Dockerfile          # Dockerfile to containerize the app
├── docker-compose.yml  # Docker Compose file for local deployment
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## AI Enhancements

The `/companies/{company_id}/ai-insights` endpoint simulates integration with a Hugging Face to analyze tweet texts and extract common issues with sentiment analysis. Analysis works with a zero-shot classification model obtained from HF to simply classify the text as a common issue. Then the text is also analyzed with a sentiment analysis model from HF to classify it as positive or negative a retrieve the general sentiment analysis.