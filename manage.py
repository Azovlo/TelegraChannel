# manage.py
"""
Скрипт управления ботом
"""
import argparse
import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent))

from main import TelegramChannelBot
from config import Config
from database.storage import Storage


async def test_parsers():
    """Тестирование парсеров"""
    print("🧪 Тестирование парсеров...\n")
    
    config = Config.load()
    bot = TelegramChannelBot(config)
    
    # Тест GitHub
    print("📊 GitHub Trending:")
    github_items = await bot.github_parser.fetch_trending('python', 'daily')
    for i, item in enumerate(github_items[:3], 1):
        print(f"{i}. {item['title']}")
        print(f"   ⭐ {item['stars']} | +{item['stars_today']} сегодня")
        print(f"   🔗 {item['url']}\n")
    
    # Тест Habr
    print("\n📚 Habr статьи:")
    habr_items = await bot.habr_parser.fetch_articles('daily', 3)
    for i, item in enumerate(habr_items, 1):
        print(f"{i}. {item['title']}")
        print(f"   👁 {item['views']} просмотров | ⬆️ {item['rating']}")
        print(f"   🔗 {item['url']}\n")


async def test_ai():
    """Тестирование AI обработки"""
    print("🤖 Тестирование AI обработки...\n")
    
    config = Config.load()
    bot = TelegramChannelBot(config)
    
    # Тестовый контент
    test_content = {
        'title': 'awesome-python',
        'description': 'A curated list of awesome Python frameworks, libraries, software and resources',
        'url': 'https://github.com/vinta/awesome-python',
        'source': 'github'
    }
    
    processed = await bot.ai_processor.process_post(
        title=test_content['title'],
        description=test_content['description'],
        url=test_content['url'],
        source=test_content['source']
    )
    
    print("Обработанный пост:")
    print("=" * 50)
    print(processed['formatted_text'])
    print("=" * 50)


async def show_stats():
    """Показать статистику"""
    print("📊 Статистика публикаций\n")
    
    config = Config.load()
    storage = Storage(config.database_path)
    
    # Статистика за 7 дней
    stats_7d = storage.get_statistics(7)
    print(f"За последние 7 дней:")
    print(f"  Всего постов: {stats_7d['total']}")
    print(f"  GitHub: {stats_7d['github']}")
    print(f"  Habr: {stats_7d['habr']}")
    
    # Статистика за 30 дней
    stats_30d = storage.get_statistics(30)
    print(f"\nЗа последние 30 дней:")
    print(f"  Всего постов: {stats_30d['total']}")
    print(f"  GitHub: {stats_30d['github']}")
    print(f"  Habr: {stats_30d['habr']}")
    
    # Последние посты
    print(f"\n📝 Последние 5 постов:")
    last_posts = storage.get_last_published(5)
    for i, post in enumerate(last_posts, 1):
        print(f"{i}. [{post['source']}] {post['title']}")
        print(f"   {post['published_at']}")


async def cleanup_db(days: int = 90):
    """Очистка старых записей"""
    print(f"🧹 Очистка записей старше {days} дней...")
    
    config = Config.load()
    storage = Storage(config.database_path)
    
    deleted = storage.cleanup_old_records(days)
    print(f"✅ Удалено записей: {deleted}")


def main():
    parser = argparse.ArgumentParser(description='Управление Telegram Channel Bot')
    subparsers = parser.add_subparsers(dest='command', help='Команды')
    
    # Команды
    subparsers.add_parser('test-parsers', help='Тестирование парсеров')
    subparsers.add_parser('test-ai', help='Тестирование AI обработки')
    subparsers.add_parser('stats', help='Показать статистику')
    
    cleanup_parser = subparsers.add_parser('cleanup', help='Очистить старые записи')
    cleanup_parser.add_argument('--days', type=int, default=90, help='Удалить записи старше N дней')
    
    args = parser.parse_args()
    
    if args.command == 'test-parsers':
        asyncio.run(test_parsers())
    elif args.command == 'test-ai':
        asyncio.run(test_ai())
    elif args.command == 'stats':
        asyncio.run(show_stats())
    elif args.command == 'cleanup':
        asyncio.run(cleanup_db(args.days))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
