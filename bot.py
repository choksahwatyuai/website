#!/usr/bin/env python3
import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные окружения
load_dotenv()

# Настраиваем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables!")

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
if not WEBHOOK_URL:
    raise ValueError("No WEBHOOK_URL found in environment variables!")

# Клавиатура для основного меню
MAIN_KEYBOARD = ReplyKeyboardMarkup([
    ['🌿 О Cerbera Odollam', '📦 Доставка'],
    ['💊 Эффекты', '📝 История'],
    ['📞 Контакт', '❓ Помощь']
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_message = (
        "🌿 *Добро пожаловать в мир Cerbera Odollam* 🌿\n\n"
        "Я специализированный бот по информации о редком растении из Юго-Восточной Азии "
        "и его безопасной доставке в любую точку мира.\n\n"
        "*Доступные команды:*\n"
        "• /about - Узнать о Cerbera Odollam\n"
        "• /delivery - Информация о доставке\n"
        "• /effects - Эффекты и воздействие\n"
        "• /history - История использования\n"
        "• /contact - Связаться с нами\n\n"
        "⚠️ _Вся информация предоставляется исключительно в образовательных целях_"
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=MAIN_KEYBOARD)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = (
        "🔍 *Как использовать бота:*\n\n"
        "1. Используйте кнопки меню или команды:\n"
        "• /about - Информация о растении\n"
        "• /delivery - Условия доставки\n"
        "• /effects - Подробное описание эффектов\n"
        "• /history - Историческая справка\n"
        "• /contact - Контактная информация\n\n"
        "2. Можете писать свои вопросы в чат\n"
        "3. Для заказа доставки используйте /delivery\n\n"
        "_Бот ответит на любые вопросы о Cerbera Odollam_"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /about"""
    about_text = (
        "🌿 *Cerbera Odollam* 🌿\n\n"
        "*Описание:*\n"
        "Редкое вечнозелёное дерево семейства Кутровых, произрастающее в мангровых лесах "
        "Индии и Юго-Восточной Азии. Известно своими уникальными свойствами и богатой историей.\n\n"
        "*Характеристики:*\n"
        "• Высота: до 12 метров\n"
        "• Цветы: белые, душистые\n"
        "• Плоды: овальные, 5-7 см\n"
        "• Семена: высокое содержание алкалоидов\n\n"
        "*Применение в истории:*\n"
        "• Традиционная медицина\n"
        "• Ритуальные церемонии\n"
        "• Научные исследования\n\n"
        "⚠️ _Информация предоставлена в образовательных целях_"
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def delivery_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /delivery"""
    delivery_text = (
        "📦 *Информация о доставке* 📦\n\n"
        "*Условия доставки:*\n"
        "• Доставка в любую точку мира\n"
        "• Полная анонимность\n"
        "• Надежная упаковка\n"
        "• Гарантия сохранности\n\n"
        "*Способы доставки:*\n"
        "• Почтовые службы\n"
        "• Курьерские службы\n"
        "• Экспресс-доставка\n\n"
        "*Сроки:*\n"
        "• Стандарт: 14-21 день\n"
        "• Экспресс: 7-10 дней\n\n"
        "💡 _Для заказа напишите в личные сообщения_"
    )
    await update.message.reply_text(delivery_text, parse_mode='Markdown')

async def effects_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /effects"""
    effects_text = (
        "💊 *Эффекты Cerbera Odollam* 💊\n\n"
        "*Активные компоненты:*\n"
        "• Цербергин\n"
        "• Неригин\n"
        "• Танкгинин\n"
        "• Дезацетилтанкгинин\n\n"
        "*Воздействие на организм:*\n"
        "• Блокировка Na⁺/K⁺-АТФазы\n"
        "• Нарушение ионного обмена\n"
        "• Влияние на сердечную мышцу\n"
        "• Необратимые изменения\n\n"
        "⚠️ _Вся информация предоставлена исключительно в научных целях_"
    )
    await update.message.reply_text(effects_text, parse_mode='Markdown')

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /history"""
    history_text = (
        "📝 *История Cerbera Odollam* 📝\n\n"
        "*Древние времена:*\n"
        "• Использование в ритуалах\n"
        "• Традиционная медицина\n"
        "• Культурное значение\n\n"
        "*Современная история:*\n"
        "• Научные исследования\n"
        "• Документированные случаи\n"
        "• Криминалистические отчеты\n\n"
        "*Интересные факты:*\n"
        "• Более 500 случаев в Керале\n"
        "• Сложность обнаружения\n"
        "• Уникальный механизм действия\n\n"
        "🔍 _История, достойная изучения_"
    )
    await update.message.reply_text(history_text, parse_mode='Markdown')

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /contact"""
    contact_text = (
        "📞 *Контактная информация* 📞\n\n"
        "*Для заказа и консультаций:*\n"
        "• Телефон: +66817045097\n"
        "• Время работы: 24/7\n"
        "• Конфиденциальность гарантируется\n\n"
        "💡 _Отвечаем в течение часа_"
    )
    await update.message.reply_text(contact_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех текстовых сообщений"""
    text = update.message.text.lower()
    
    if "доставка" in text or "📦" in text:
        await delivery_command(update, context)
    elif "эффект" in text or "действие" in text or "💊" in text:
        await effects_command(update, context)
    elif "история" in text or "📝" in text:
        await history_command(update, context)
    elif "контакт" in text or "связь" in text or "📞" in text:
        await contact_command(update, context)
    elif "cerbera" in text or "одоллам" in text or "🌿" in text:
        await about_command(update, context)
    else:
        response = (
            "*Как я могу помочь?*\n\n"
            "Выберите интересующий раздел:\n"
            "• 🌿 О растении\n"
            "• 📦 Доставка\n"
            "• 💊 Эффекты\n"
            "• 📝 История\n"
            "• 📞 Контакт\n\n"
            "_Используйте кнопки меню или команды_"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

def main():
    """Основная функция"""
    try:
        # Создаём приложение бота
        application = Application.builder().token(TOKEN).build()

        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("delivery", delivery_command))
        application.add_handler(CommandHandler("effects", effects_command))
        application.add_handler(CommandHandler("history", history_command))
        application.add_handler(CommandHandler("contact", contact_command))
        
        # Добавляем обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Настраиваем webhook
        port = int(os.getenv('PORT', 8080))
        logger.info(f"Setting webhook to {WEBHOOK_URL}")
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=WEBHOOK_URL,
            secret_token="your-secret-path",  # Добавляем секретный токен
            drop_pending_updates=True  # Игнорируем старые обновления
        )
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    main() 