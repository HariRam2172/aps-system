FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install ALL dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of code
COPY . .

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8080"]