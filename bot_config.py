# config.py
"""
Конфигурация бота
"""
import os
from dataclasses import dataclass
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Класс конфигурации бота"""
    
    # Telegram
    telegram_bot_token: str
    channel_id: str  # ID канала, например @mychannel или -1001234567890
    
    # AI API (Claude или OpenAI)
    ai_api_key: str
    ai_provider: str = 'claude'  # 'claude' или 'openai'
    
    # База данных
    database_path: str = 'bot_data.db'
    
    # Источники контента
    sources: Dict = None
    
    # GitHub настройки
    github_language: str = 'python'  # all, python, javascript и т.д.
    github_period: str = 'daily'     # daily, weekly, monthly
    
    # Habr настройки
    habr_period: str = 'daily'       # daily, weekly, monthly
    habr_limit: int = 10
    
    # Публикация
    posts_per_cycle: int = 3         # Сколько постов публиковать за раз
    delay_between_posts: int = 300   # Задержка между постами (секунды)
    posting_interval_hours: int = 6  # Интервал между циклами (часы)
    
    # Режим работы
    run_mode: str = 'continuous'     # 'once' или 'continuous'
    
    @classmethod
    def load(cls):
        """Загрузка конфигурации из переменных окружения"""
        return cls(
            telegram_bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
            channel_id=os.getenv('CHANNEL_ID'),
            ai_api_key=os.getenv('AI_API_KEY'),
            ai_provider=os.getenv('AI_PROVIDER', 'claude'),
            database_path=os.getenv('DATABASE_PATH', 'bot_data.db'),
            sources={
                'github_enabled': os.getenv('GITHUB_ENABLED', 'true').lower() == 'true',
                'habr_enabled': os.getenv('HABR_ENABLED', 'true').lower() == 'true',
            },
            github_language=os.getenv('GITHUB_LANGUAGE', 'python'),
            github_period=os.getenv('GITHUB_PERIOD', 'daily'),
            habr_period=os.getenv('HABR_PERIOD', 'daily'),
            habr_limit=int(os.getenv('HABR_LIMIT', '10')),
            posts_per_cycle=int(os.getenv('POSTS_PER_CYCLE', '3')),
            delay_between_posts=int(os.getenv('DELAY_BETWEEN_POSTS', '300')),
            posting_interval_hours=int(os.getenv('POSTING_INTERVAL_HOURS', '6')),
            run_mode=os.getenv('RUN_MODE', 'continuous'),
        )


# requirements.txt
"""
python-telegram-bot==21.0
aiohttp==3.9.1
beautifulsoup4==4.12.2
python-dotenv==1.0.0
anthropic==0.18.1
lxml==5.1.0
fake-useragent==1.4.0
"""

# .env.example
"""
# Telegram настройки
TELEGRAM_BOT_TOKEN=your_bot_token_here
CHANNEL_ID=@your_channel_or_chat_id

# AI API ключ (Claude или OpenAI)
AI_API_KEY=your_ai_api_key_here
AI_PROVIDER=claude

# База данных
DATABASE_PATH=bot_data.db

# Источники
GITHUB_ENABLED=true
HABR_ENABLED=true

# GitHub настройки
GITHUB_LANGUAGE=python
GITHUB_PERIOD=daily

# Habr настройки
HABR_PERIOD=daily
HABR_LIMIT=10

# Публикация
POSTS_PER_CYCLE=3
DELAY_BETWEEN_POSTS=300
POSTING_INTERVAL_HOURS=6

# Режим работы: once или continuous
RUN_MODE=continuous
"""
