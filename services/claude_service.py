import anthropic
import os
import logging
from typing import List, Dict, Tuple
from anthropic import AsyncAnthropic
from utils.prompt_template import SYSTEM_PROMPT, TOPIC_CLASSIFICATION_PROMPT

logger = logging.getLogger(__name__)

class ClaudeService:
    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY не найден")
            
        if not api_key.startswith('sk-ant-api03-'):
            api_key = f'sk-ant-api03-{api_key}'
            
        self.client = AsyncAnthropic(api_key=api_key, max_retries=3)
        self.model = "claude-3-sonnet-20240229"

    async def classify_topic(self, message: str) -> str:
        try:
            response = await self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": f"{message}\n\n{TOPIC_CLASSIFICATION_PROMPT}"}],
                max_tokens=100,
                temperature=0.3
            )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Ошибка классификации: {e}")
            return "Другое"

    async def get_response(self, message: str, history: List[Dict] = None) -> Tuple[str, str]:
        try:
            # Сначала определяем тему
            topic = await self.classify_topic(message)
            
            # Формируем диалог
            messages = []
            if history:
                for msg in history:
                    try:
                        role = 'assistant' if msg['fields']['role'] == 'assistant' else 'user'
                        messages.append({
                            "role": role,
                            "content": msg['fields']['message']
                        })
                    except KeyError as e:
                        logger.error(f"Ошибка в истории: {e}")
                        continue
            
            messages.append({"role": "user", "content": message})

            response = await self.client.messages.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                system=SYSTEM_PROMPT
            )
            
            return response.content[0].text, topic

        except Exception as e:
            logger.error(f"Ошибка Claude: {e}")
            return "Извините, произошла ошибка при обработке вашего запроса.", "Другое"
