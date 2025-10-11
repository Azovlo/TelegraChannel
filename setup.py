#!/usr/bin/env python3
"""
Скрипт настройки Telegram Channel Bot
"""
import os
import shutil
from pathlib import Path

def create_env_file():
    """Создание .env файла из примера"""
    if os.path.exists('.env'):
        print("✅ Файл .env уже существует")
        return
    
    if os.path.exists('env.example'):
        shutil.copy('env.example', '.env')
        print("✅ Создан файл .env из env.example")
        print("📝 Не забудьте отредактировать .env файл с вашими настройками!")
    else:
        print("❌ Файл env.example не найден")

def create_directories():
    """Создание необходимых директорий"""
    dirs = ['data', 'logs']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Создана директория: {dir_name}")

def show_next_steps():
    """Показать следующие шаги"""
    print("\n🎯 Следующие шаги:")
    print("1. Отредактируйте файл .env с вашими настройками")
    print("2. Установите зависимости: pip install -r requirements.txt")
    print("3. Запустите бота: python run.py")
    print("\n📖 Подробная документация в README.md")

def main():
    """Главная функция"""
    print("🚀 Настройка Telegram Channel Bot")
    print("=" * 40)
    
    create_directories()
    create_env_file()
    show_next_steps()

if __name__ == '__main__':
    main()
