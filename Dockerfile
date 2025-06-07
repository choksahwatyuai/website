FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY . .

# Установка Python HTTP сервера
RUN pip install http.server

# Открываем порт
EXPOSE 8080

# Создаем скрипт для запуска обоих процессов
RUN echo '#!/bin/bash\npython -m http.server 8080 & python bot.py' > start.sh
RUN chmod +x start.sh

# Запускаем оба процесса
CMD ["./start.sh"] 