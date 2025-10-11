# database/storage.py
"""
База данных для хранения информации о публикациях
"""
import sqlite3
from datetime import datetime
from typing import Optional


class Storage:
    """Класс для работы с базой данных"""
    
    def __init__(self, db_path: str = 'bot_data.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица опубликованных постов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS published_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                published_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Индекс для быстрого поиска по URL
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_url ON published_posts(url)
        ''')
        
        # Таблица статистики
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                posts_published INTEGER DEFAULT 0,
                github_posts INTEGER DEFAULT 0,
                habr_posts INTEGER DEFAULT 0,
                errors INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def is_published(self, url: str) -> bool:
        """
        Проверка, был ли пост уже опубликован
        
        Args:
            url: URL поста
        
        Returns:
            True если пост уже публиковался
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM published_posts WHERE url = ?', (url,))
        result = cursor.fetchone()
        
        conn.close()
        return result is not None
    
    def mark_as_published(self, url: str, title: str, published_at: datetime, source: str = 'unknown'):
        """
        Отметить пост как опубликованный
        
        Args:
            url: URL поста
            title: Заголовок поста
            published_at: Время публикации
            source: Источник (github/habr)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO published_posts (url, title, source, published_at)
                VALUES (?, ?, ?, ?)
            ''', (url, title, source, published_at))
            
            conn.commit()
        except sqlite3.IntegrityError:
            # URL уже существует в базе
            pass
        finally:
            conn.close()
    
    def get_published_count(self, days: int = 7) -> int:
        """
        Получить количество опубликованных постов за последние N дней
        
        Args:
            days: Количество дней
        
        Returns:
            Количество постов
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM published_posts
            WHERE published_at >= datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        result = cursor.fetchone()[0]
        conn.close()
        
        return result
    
    def get_statistics(self, days: int = 7) -> dict:
        """
        Получить статистику публикаций
        
        Args:
            days: Количество дней для статистики
        
        Returns:
            Словарь со статистикой
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Общее количество
        cursor.execute('''
            SELECT COUNT(*) FROM published_posts
            WHERE published_at >= datetime('now', '-' || ? || ' days')
        ''', (days,))
        total = cursor.fetchone()[0]
        
        # По источникам
        cursor.execute('''
            SELECT source, COUNT(*) FROM published_posts
            WHERE published_at >= datetime('now', '-' || ? || ' days')
            GROUP BY source
        ''', (days,))
        by_source = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total': total,
            'github': by_source.get('github', 0),
            'habr': by_source.get('habr', 0),
            'days': days
        }
    
    def get_last_published(self, limit: int = 10) -> list:
        """
        Получить последние опубликованные посты
        
        Args:
            limit: Максимальное количество постов
        
        Returns:
            Список последних постов
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT url, title, source, published_at
            FROM published_posts
            ORDER BY published_at DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'url': row[0],
                'title': row[1],
                'source': row[2],
                'published_at': row[3]
            }
            for row in results
        ]
    
    def cleanup_old_records(self, days: int = 90):
        """
        Очистка старых записей из базы данных
        
        Args:
            days: Удалить записи старше N дней
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM published_posts
            WHERE published_at < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted
