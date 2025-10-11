"""
Telegram Channel Automation Bot
Автоматизированная система для ведения Telegram-канала
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict
import random

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

from bot_config import Config
from parsers.github_parser import GitHubParser
from parsers.habr_parser import HabrParser
from ai.content_processor import ContentProcessor
from database.storage import Storage

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelegramChannelBot:
    """Основной класс бота для автоматизации Telegram-канала"""
    
    def __init__(self, config: Config):
        self.config = config
        self.bot = Bot(token=config.telegram_bot_token)
        self.github_parser = GitHubParser()
        self.habr_parser = HabrParser()
        self.ai_processor = ContentProcessor(config.ai_api_key)
        self.storage = Storage(config.database_path)
        
    async def collect_content(self) -> List[Dict]:
        """Сбор контента из всех источников"""
        logger.info("Начинаем сбор контента...")
        content_items = []
        
        try:
            # Парсинг GitHub Trending
            if self.config.sources.get('github_enabled', True):
                logger.info("Парсинг GitHub Trending...")
                github_items = await self.github_parser.fetch_trending(
                    language=self.config.github_language,
                    period=self.config.github_period
                )
                content_items.extend(github_items)
                logger.info(f"Собрано {len(github_items)} проектов с GitHub")
            
            # Парсинг Habr
            if self.config.sources.get('habr_enabled', True):
                logger.info("Парсинг Habr...")
                habr_items = await self.habr_parser.fetch_articles(
                    period=self.config.habr_period,
                    limit=self.config.habr_limit
                )
                content_items.extend(habr_items)
                logger.info(f"Собрано {len(habr_items)} статей с Habr")
                
        except Exception as e:
            logger.error(f"Ошибка при сборе контента: {e}")
            
        return content_items
    
    async def process_content(self, content_item: Dict) -> Dict:
        """Обработка контента через AI"""
        try:
            # Проверяем, не публиковали ли мы это раньше
            if self.storage.is_published(content_item['url']):
                logger.info(f"Контент уже был опубликован: {content_item['title']}")
                return None
            
            # AI обработка: рерайтинг и добавление эмодзи
            processed = await self.ai_processor.process_post(
                title=content_item['title'],
                description=content_item.get('description', ''),
                url=content_item['url'],
                source=content_item['source']
            )
            
            return processed
            
        except Exception as e:
            logger.error(f"Ошибка при обработке контента: {e}")
            return None
    
    async def publish_post(self, post_data: Dict) -> bool:
        """Публикация поста в Telegram-канал"""
        try:
            message = post_data['formatted_text']
            
            # Публикация в канал
            await self.bot.send_message(
                chat_id=self.config.channel_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=False
            )
            
            # Сохраняем информацию о публикации
            self.storage.mark_as_published(
                url=post_data['url'],
                title=post_data['title'],
                published_at=datetime.now(),
                source=post_data['source']
            )
            
            logger.info(f"Пост опубликован: {post_data['title']}")
            return True
            
        except TelegramError as e:
            logger.error(f"Ошибка Telegram при публикации: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при публикации поста: {e}")
            return False
    
    async def run_posting_cycle(self):
        """Один цикл работы бота: сбор, обработка и публикация"""
        logger.info("=" * 50)
        logger.info("Запуск цикла публикации")
        logger.info("=" * 50)
        
        # Сбор контента
        content_items = await self.collect_content()
        
        if not content_items:
            logger.warning("Не найдено контента для публикации")
            return
        
        # Перемешиваем для разнообразия
        random.shuffle(content_items)
        
        # Обрабатываем и публикуем
        posts_published = 0
        for item in content_items[:self.config.posts_per_cycle]:
            processed = await self.process_content(item)
            
            if processed:
                success = await self.publish_post(processed)
                if success:
                    posts_published += 1
                    
                    # Задержка между постами
                    if posts_published < self.config.posts_per_cycle:
                        delay = self.config.delay_between_posts
                        logger.info(f"Ожидание {delay} секунд перед следующим постом...")
                        await asyncio.sleep(delay)
        
        logger.info(f"Цикл завершен. Опубликовано постов: {posts_published}")
    
    async def run_continuous(self):
        """Непрерывная работа бота с заданным интервалом"""
        logger.info("Бот запущен в непрерывном режиме")
        logger.info(f"Интервал между циклами: {self.config.posting_interval_hours} часов")
        
        while True:
            try:
                await self.run_posting_cycle()
                
                # Ожидание до следующего цикла
                interval_seconds = self.config.posting_interval_hours * 3600
                next_run = datetime.now().timestamp() + interval_seconds
                next_run_time = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
                
                logger.info(f"Следующий запуск в: {next_run_time}")
                await asyncio.sleep(interval_seconds)
                
            except KeyboardInterrupt:
                logger.info("Получен сигнал остановки")
                break
            except Exception as e:
                logger.error(f"Неожиданная ошибка в основном цикле: {e}")
                logger.info("Повтор через 5 минут...")
                await asyncio.sleep(300)


async def main():
    """Точка входа в приложение"""
    # Загрузка конфигурации
    config = Config.load()
    
    # Создание и запуск бота
    bot = TelegramChannelBot(config)
    
    # Выбор режима работы
    if config.run_mode == 'once':
        logger.info("Режим: одноразовый запуск")
        await bot.run_posting_cycle()
    else:
        logger.info("Режим: непрерывная работа")
        await bot.run_continuous()


if __name__ == '__main__':
    asyncio.run(main())
