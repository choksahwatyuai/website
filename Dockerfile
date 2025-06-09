FROM python:3.9-slim

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    tree \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем сначала только requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Убеждаемся, что все файлы имеют правильные права доступа
RUN chmod -R 755 /app

# Удаляем ненужные файлы
RUN rm -f session_data.pickle session_manager.py

# Проверяем наличие всех необходимых файлов
RUN echo "=== Directory Structure ===" && \
    tree /app && \
    echo "\n=== File Permissions ===" && \
    ls -la /app && \
    echo "\n=== HTML Files ===" && \
    find /app -name "*.html" && \
    echo "\n=== CSS Files ===" && \
    find /app -name "*.css" && \
    echo "\n=== Image Files ===" && \
    find /app -type f -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" -o -name "*.webp" -o -name "*.ico" -o -name "*.jfif"

# Указываем порт
ENV PORT=8080
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Запускаем сервер
CMD ["python", "server.py"] 