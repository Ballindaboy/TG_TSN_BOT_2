from anthropic import Anthropic
from telegram import Update
from telegram.ext import ContextTypes
from utils.prompt_template import SYSTEM_PROMPT
import os
from dotenv import load_dotenv
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Создаем клиент Anthropic с явным указанием api_key
api_key = os.getenv('CLAUDE_API_KEY')
if not api_key:
    raise ValueError("CLAUDE_API_KEY не найден в переменных окружения")

anthropic = Anthropic(api_key=api_key)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик сообщений"""
    try:
        message = update.message.text
        user = update.effective_user
        logger.info(f"Получено сообщение от {user.id}: {message}")
        
        # Отправляем сообщение о том, что бот думает
        processing_message = await update.message.reply_text(
            "Получил ваше сообщение, обрабатываю..."
        )
        
        # Создаем запрос к Claude
        response = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": message
            }]
        )
        
        # Удаляем сообщение о обработке
        await processing_message.delete()
        
        # Проверяем ответ
        if not response or not response.content:
            raise ValueError("Получен пустой ответ от Claude API")
            
        # Отправляем ответ
        await update.message.reply_text(response.content[0].text)
        logger.info(f"Отправлен ответ пользователю {user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await update.message.reply_text("Произошла ошибка при обработке сообщения")