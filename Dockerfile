FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc python3-dev libpq-dev libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Rodar tudo em um único processo
CMD ["python", "main.py"]
