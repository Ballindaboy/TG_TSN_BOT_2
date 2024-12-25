import os
from dotenv import load_dotenv
import logging
import asyncio
import platform
import nest_asyncio

# Загружаем переменные окружения ДО импорта других модулей
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Применяем патч для вложенных event loops
nest_asyncio.apply()

# Проверяем загрузку переменных
logger.info(f"AIRTABLE_BASE_ID: {os.getenv('AIRTABLE_BASE_ID')}")
logger.info(f"AIRTABLE_API_KEY: {'Установлен' if os.getenv('AIRTABLE_API_KEY') else 'Не установлен'}")
logger.info(f"AIRTABLE_CONVERSATIONS_TABLE: {os.getenv('AIRTABLE_CONVERSATIONS_TABLE')}")
logger.info(f"AIRTABLE_MESSAGES_TABLE: {os.getenv('AIRTABLE_MESSAGES_TABLE')}")

# Теперь импортируем остальные модули
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.message_handler import handle_message
from handlers.command_handler import start_command

def run():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Бот запущен и ожидает сообщений...")
    
    # Запускаем бота
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    try:
        # Сначала установите: pip install nest-asyncio
        run()
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True) 