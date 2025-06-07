FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаем два разных CMD для веб-сервера и бота
CMD ["sh", "-c", "python -m http.server 8080 & python bot.py"] 