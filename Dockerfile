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
echo "Starting web server..."\n\
python server.py & \
echo "Starting Telegram bot..."\n\
python bot.py' > /app/start.sh

# Делаем скрипт исполняемым
RUN chmod +x /app/start.sh

# Проверяем наличие всех необходимых файлов
RUN ls -la && \
    echo "Content of start.sh:" && \
    cat /app/start.sh

# Указываем порт
ENV PORT=8080
EXPOSE 8080

# Запускаем сервисы
CMD ["/bin/bash", "/app/start.sh"] 