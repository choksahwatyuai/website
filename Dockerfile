FROM python:3.9-slim

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем сначала только requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаем необходимые директории
RUN mkdir -p static templates

# Копируем файлы проекта
COPY static/ static/
COPY templates/ templates/
COPY server.py bot.py config.py ./

# Убеждаемся, что все файлы имеют правильные права доступа
RUN chmod -R 755 /app

# Удаляем ненужные файлы
RUN rm -f session_data.pickle session_manager.py

# Проверяем наличие всех необходимых файлов
RUN ls -la && \
    echo "Files in /app:" && \
    ls -la /app && \
    echo "Files in /app/static:" && \
    ls -la /app/static && \
    echo "Files in /app/templates:" && \
    ls -la /app/templates

# Указываем порт
ENV PORT=8080
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Запускаем сервер
CMD ["python", "server.py"] 