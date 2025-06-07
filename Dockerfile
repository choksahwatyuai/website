FROM python:3.9-slim

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY . .

# Создаем скрипт запуска
RUN echo '#!/bin/bash\n\
echo "Starting services..."\n\
python -m http.server ${PORT:-8080} & \
python bot.py\n\
wait' > /app/start.sh

# Делаем скрипт исполняемым
RUN chmod +x /app/start.sh

# Указываем порт
EXPOSE ${PORT:-8080}

# Запускаем сервисы
CMD ["/app/start.sh"] 