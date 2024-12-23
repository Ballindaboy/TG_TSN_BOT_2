from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    try:
        await update.message.reply_text(
            "Здравствуйте! Я - ваш помощник по вопросам управления ТСН/ТСЖ. "
            "Задавайте вопросы, и я помогу вам с юридической и административной информацией."
        )
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}") 