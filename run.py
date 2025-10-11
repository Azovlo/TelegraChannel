#!/usr/bin/env python3
"""
Скрипт быстрого запуска Telegram Channel Bot
"""
import os
import sys
import asyncio
from pathlib import Path

def check_env_file():
    """Проверка наличия .env файла"""
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("📝 Создайте файл .env на основе env.example:")
        print("   cp env.example .env")
        print("   # Затем отредактируйте .env файл с вашими настройками")
        return False
    return True

def check_dependencies():
    """Проверка установленных зависимостей"""
    try:
        import telegram
        import aiohttp
        import anthropic
        import bs4
        return True
    except ImportError as e:
        print(f"❌ Не установлены зависимости: {e}")
        print("📦 Установите зависимости:")
        print("   pip install -r requirements.txt")
        return False

async def main():
    """Главная функция"""
    print("🤖 Telegram Channel Bot")
    print("=" * 40)
    
    # Проверки
    if not check_env_file():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Импорт и запуск
    try:
        from main import main as bot_main
        print("✅ Все проверки пройдены, запускаем бота...")
        await bot_main()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
