# ТСН Помощник Бот

Telegram бот-ассистент для председателей ТСН/ТСЖ, использующий AI (Claude) для предоставления юридических и административных консультаций.

## Описание

Бот предназначен для помощи председателям ТСН/ТСЖ в решении повседневных задач управления. Использует AI-модель Claude для предоставления актуальной информации на основе законодательства РФ и нормативных актов Ульяновской области.

## Основные функции

- ✅ Консультации по юридическим вопросам ТСН/ТСЖ
- ✅ Ссылки на актуальные нормативные акты и законы
- ✅ Рекомендации по безопасному управлению ТСН
- ✅ Сохранение истории переписки в Airtable
- ✅ Автоматическая классификация тем обращений
- 🔄 Управление документацией ТСН (в разработке)

## Возможности AI-ассистента

- Предоставление информации на основе актуального законодательства
- Ссылки на конкретные статьи законов и нормативных актов
- Рекомендации по безопасному ведению деятельности
- Помощь в административных вопросах
- Предупреждение о потенциальных рисках
- Классификация тем обращений

## Технологии

- Python 3.13
- python-telegram-bot
- Anthropic Claude 3 Sonnet
- Airtable API
- python-dotenv
- nest-asyncio (для Windows)

## Требования

- Python 3.13 или выше
- Telegram Bot Token
- Claude API Key (начинается с sk-ant-api03-)
- Airtable API Key и Base ID

## Установка

1. Клонировать репозиторий
2. Установить зависимости: `pip install -r requirements.txt`
3. Создать файл `.env` и заполнить необходимые переменные
4. Запустить бот: `python main.py`

## Настройка окружения

Создайте файл `.env` в корневой директории проекта:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Claude API
ANTHROPIC_API_KEY=your_claude_api_key

# Airtable
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_CONVERSATIONS_TABLE=TSN_CONV
AIRTABLE_MESSAGES_TABLE=TSN_MSG
```

## Структура Airtable

### TSN_CONV (Диалоги)
- user_id (Number)
- start_time (DateTime)
- last_message_time (DateTime)
- topic (Single line text)
- status (Single line text)

### TSN_MSG (Сообщения)
- conversation_id (Link to TSN_CONV)
- user_id (Number)
- message (Long text)
- role (Single line text)
- timestamp (DateTime)
- topic_classification (Single line text)

## Планируемые улучшения

- [x] Интеграция с Airtable для хранения истории переписки
- [x] Автоматическая классификация тем
- [ ] Система управления документами ТСН
- [ ] База знаний с часто задаваемыми вопросами
- [ ] Календарь важных дат и напоминаний
- [ ] Шаблоны документов

## Структура проекта

```
project/
├── README.md
├── requirements.txt
├── .env
├── main.py
├── handlers/
│   ├── __init__.py
│   ├── message_handler.py
│   └── command_handler.py
├── utils/
│   ├── __init__.py
│   └── prompt_template.py
├── services/
│   ├── __init__.py
│   ├── airtable_service.py
│   └── claude_service.py
└── database/
    ├── __init__.py
    └── models.py