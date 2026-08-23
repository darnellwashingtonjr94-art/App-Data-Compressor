FROM python:3.11-slim
WORKDIR /app

# Copy dependency manifest first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

CMD ["uvicorn", "src.api_gateway:app", "--host", "0.0.0.0", "--port", "8000"]
