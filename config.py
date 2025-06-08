import os

# Установка переменных окружения
os.environ.setdefault('TELEGRAM_BOT_TOKEN', os.getenv('TELEGRAM_BOT_TOKEN', ''))
os.environ.setdefault('WEBHOOK_URL', os.getenv('WEBHOOK_URL', ''))
os.environ.setdefault('PORT', os.getenv('PORT', '8080')) 