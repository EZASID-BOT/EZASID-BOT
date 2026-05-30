FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends poppler-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV BOT_TOKEN=${BOT_TOKEN}
ENV TOKEN=${TOKEN}
ENV GEMINI_API_KEY=${GEMINI_API_KEY}
ENV API_KEY=${API_KEY}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
