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
\n\
# Ждем запуска сервера\n\
echo "Waiting for server to start..."\n\
sleep 5\n\
\n\
# Проверяем доступность сервера\n\
if ! curl -f http://localhost:${PORT:-8080}/health; then\n\
    echo "Server health check failed"\n\
    exit 1\n\
fi\n\
\n\
echo "Server is healthy, starting bot..."\n\
python bot.py & BOT_PID=$!\n\
\n\
# Функция для корректного завершения процессов\n\
cleanup() {\n\
    echo "Shutting down..."\n\
    kill $SERVER_PID $BOT_PID 2>/dev/null\n\
    exit 0\n\
}\n\
\n\
# Перехватываем сигналы завершения\n\
trap cleanup SIGTERM SIGINT\n\
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

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Запускаем сервисы
CMD ["/bin/bash", "/app/start.sh"] 