FROM python:3.9-slim

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
# Добавляем метку времени для предотвращения кэширования
ARG CACHEBUST=1
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir telethon==1.33.1

# Копирование файлов проекта
COPY . .

# Создаем скрипт запуска
RUN echo '#!/bin/bash\n\
echo "Starting web server..."\n\
python server.py & SERVER_PID=$!\n\
echo "Starting Telegram bot..."\n\
python bot.py & BOT_PID=$!\n\
\n\
# Ждем инициализации сервера\n\
sleep 5\n\
\n\
# Проверяем, что сервер отвечает\n\
curl -f http://localhost:${PORT:-8080}/health || exit 1\n\
\n\
# Ждем завершения процессов\n\
wait $SERVER_PID $BOT_PID' > /app/start.sh

# Делаем скрипт исполняемым
RUN chmod +x /app/start.sh

# Проверяем наличие всех необходимых файлов и зависимостей
RUN ls -la && \
    echo "Content of start.sh:" && \
    cat /app/start.sh && \
    echo "Installed packages:" && \
    pip list

# Указываем порт
ENV PORT=8080
EXPOSE 8080

# Запускаем сервисы
CMD ["/bin/bash", "/app/start.sh"] 