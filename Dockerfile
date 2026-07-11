FROM python:3.12-slim

# Instala dependências do sistema (importante para qrcode, psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["supervisord", "-c", "supervisord.conf"]
