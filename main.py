import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.message_handler import handle_message
from handlers.command_handler import start_command
import asyncio
import platform
import logging
from logging.handlers import RotatingFileHandler

# Путь к лог-файлу в зависимости от ОС
log_path = 'C:/temp/tsn_bot/bot.log' if platform.system() == 'Windows' else '/var/log/tsn_bot/bot.log'

# Создаем директорию для логов
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            log_path,
            maxBytes=10485760,
            backupCount=5,
            encoding='utf-8'
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

# Настраиваем кодировку для консоли Windows
if platform.system() == 'Windows':
    import locale
    sys.stdout.reconfigure(encoding='utf-8')
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

logger = logging.getLogger(__name__)

load_dotenv()

def check_single_instance():
    """Проверка на единственный экземпляр"""
    pid_file = 'C:/temp/tsn_bot.pid' if platform.system() == 'Windows' else '/tmp/tsn_bot.pid'
    
    if platform.system() == 'Windows':
        os.makedirs('C:/temp', exist_ok=True)
        
    if os.path.exists(pid_file):
        with open(pid_file) as f:
            pid = f.read().strip()
            try:
                os.kill(int(pid), 0)
                logger.error(f"Бот уже запущен с PID {pid}")
                sys.exit(1)
            except OSError:
                pass
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))

def run_bot():
    """Запуск бота"""
    logger.info("Бот запускается...")
    
    try:
        # Создаем приложение
        application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
        logger.info("Приложение создано успешно")

        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        logger.info("Обработчики зарегистрированы")

        # Запускаем бота
        logger.info("Бот начинает работу...")
        application.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise

if __name__ == '__main__':
    check_single_instance()
    # Специальная обработка для Windows
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    try:
        run_bot()
    except KeyboardInterrupt:
        print('Бот остановлен')
    except Exception as e:
        print(f'Произошла ошибка: {e}') 