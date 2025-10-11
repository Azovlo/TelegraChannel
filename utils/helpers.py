# utils/helpers.py
"""
Вспомогательные функции
"""
import re
from datetime import datetime


def clean_html(text: str) -> str:
    """Очистка HTML тегов из текста"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def truncate_text(text: str, max_length: int = 300) -> str:
    """Обрезка текста до указанной длины"""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'


def format_number(num: int) -> str:
    """Форматирование больших чисел (1000 -> 1K)"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def get_time_ago(published_at: datetime) -> str:
    """Получить строку 'X времени назад'"""
    now = datetime.now()
    diff = now - published_at
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "только что"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} мин. назад"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} ч. назад"
    else:
        days = int(seconds / 86400)
        return f"{days} дн. назад"
