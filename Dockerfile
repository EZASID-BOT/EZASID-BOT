FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends poppler-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Render የሞላናቸውን ቶከኖች ለዶከር ሲስተም ማስተላለፊያ
ENV BOT_TOKEN=${BOT_TOKEN}
ENV GEMINI_API_KEY=${GEMINI_API_KEY}

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

CMD ["python", "main.py"]
