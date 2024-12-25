import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.airtable_service import AirtableService
from services.claude_service import ClaudeService

logger = logging.getLogger(__name__)
airtable = AirtableService()
claude = ClaudeService()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        message = update.message.text
        
        # Получаем или создаем диалог
        conversation = context.user_data.get('current_conversation')
        if not conversation:
            conversation = airtable.create_conversation(
                user_id=user.id,
                topic="Знакомство"
            )
            context.user_data['current_conversation'] = conversation
            response = f"Здравствуйте, {user.first_name}! Я помогу вам с вопросами по управлению ТСН/ТСЖ. Какой у вас вопрос?"
            topic = "Знакомство"
        else:
            history = airtable.get_conversation_history(conversation['id'])
            response, topic = await claude.get_response(message, history)
            
            # Обновляем тему диалога
            airtable.update_conversation_topic(conversation['id'], topic)

        # Сохраняем сообщения
        airtable.add_message(
            conversation_id=conversation['id'],
            user_id=user.id,
            message=message,
            role='user',
            topic=topic
        )
        
        airtable.add_message(
            conversation_id=conversation['id'],
            user_id=0,
            message=response,
            role='assistant',
            topic=topic
        )
        
        await update.message.reply_text(response)

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("Произошла ошибка при обработке сообщения")