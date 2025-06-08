FROM python:3.9-slim

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Добавляем метку времени для предотвращения кэширования
ARG CACHEBUST=$(date +%s)
RUN echo "Cache bust: $CACHEBUST"

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Удаляем ненужные файлы
RUN rm -f session_data.pickle session_manager.py

# Создаем скрипт запуска
RUN echo '#!/bin/bash\n\
\n\
# Проверяем переменные окружения\n\
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then\n\
    echo "Error: TELEGRAM_BOT_TOKEN is not set"\n\
    exit 1\n\
fi\n\
\n\
if [ -z "$WEBHOOK_URL" ]; then\n\
    echo "Error: WEBHOOK_URL is not set"\n\
    exit 1\n\
fi\n\
\n\
# Запускаем веб-сервер\n\
echo "Starting web server..."\n\
python server.py & SERVER_PID=$!\n\
\n\
# Ждем запуска сервера\n\
echo "Waiting for server to start..."\n\
for i in {1..30}; do\n\
    if curl -s http://localhost:${PORT:-8080}/health | grep -q "healthy"; then\n\
        echo "Server is healthy"\n\
        break\n\
    fi\n\
    if [ $i -eq 30 ]; then\n\
        echo "Server failed to start"\n\
        exit 1\n\
    fi\n\
    sleep 1\n\
done\n\
\n\
# Запускаем бота\n\
echo "Starting bot..."\n\
python -u bot.py & BOT_PID=$!\n\
\n\
# Функция для корректного завершения\n\
cleanup() {\n\
    echo "Shutting down..."\n\
    kill $SERVER_PID $BOT_PID 2>/dev/null\n\
    exit 0\n\
}\n\
\n\
trap cleanup SIGTERM SIGINT\n\
\n\
# Мониторим процессы\n\
while true; do\n\
    if ! ps -p $SERVER_PID > /dev/null || ! ps -p $BOT_PID > /dev/null; then\n\
        echo "One of the processes died"\n\
        cleanup\n\
    fi\n\
    sleep 5\n\
done' > /app/start.sh

# Делаем скрипт исполняемым
RUN chmod +x /app/start.sh

# Проверяем наличие всех необходимых файлов и зависимостей
RUN ls -la && \
    echo "Content of start.sh:" && \
    cat /app/start.sh && \
    echo "Installed packages:" && \
    pip list && \
    echo "Files in /app:" && \
    ls -la /app

# Указываем порт
ENV PORT=8080
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Запускаем сервисы
CMD ["/bin/bash", "/app/start.sh"] 