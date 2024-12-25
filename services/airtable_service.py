from airtable import Airtable
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AirtableService:
    def __init__(self):
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        self.api_key = os.getenv('AIRTABLE_API_KEY')
        
        if not self.base_id or not self.api_key:
            raise ValueError("AIRTABLE_BASE_ID или AIRTABLE_API_KEY не найдены в переменных окружения")
            
        self.conversations_table = os.getenv('AIRTABLE_CONVERSATIONS_TABLE')
        self.messages_table = os.getenv('AIRTABLE_MESSAGES_TABLE')
        
        if not self.conversations_table or not self.messages_table:
            raise ValueError("AIRTABLE_CONVERSATIONS_TABLE или AIRTABLE_MESSAGES_TABLE не найдены")
            
        self.conversations = Airtable(
            self.base_id, 
            self.conversations_table,
            self.api_key
        )
        self.messages = Airtable(
            self.base_id, 
            self.messages_table,
            self.api_key
        )

    def create_conversation(self, user_id, topic):
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        return self.conversations.insert({
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'last_message_time': datetime.now().isoformat(),
            'topic': topic,
            'status': 'active'
        })

    def add_message(self, conversation_id, user_id, message, role, topic):
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        return self.messages.insert({
            'conversation_id': [conversation_id],
            'user_id': user_id,
            'message': message,
            'role': role,
            'timestamp': datetime.now().isoformat(),
            'topic_classification': topic
        })

    def get_conversation_history(self, conversation_id, limit=5):
        return self.messages.search('conversation_id', conversation_id, sort=[('timestamp', 'desc')], max_records=limit)

    def update_conversation_topic(self, conversation_id: str, topic: str):
        """Обновляет тему диалога"""
        try:
            self.conversations.update(conversation_id, {'topic': topic})
        except Exception as e:
            logger.error(f"Ошибка обновления темы: {e}")
