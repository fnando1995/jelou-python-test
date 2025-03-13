FROM python:3.12-slim

# Set working directory
WORKDIR /jelou

# Copy application code
COPY ./app ./app
COPY ./tests ./tests
# Copy requirements and install dependencies
COPY ./requirements.txt .
COPY ./.env .
RUN pip install --upgrade pip && pip install -r requirements.txt
# Set working directory
WORKDIR /jelou/app
# Expose port 8000
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
