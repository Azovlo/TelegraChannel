# ai/content_processor.py
"""
AI обработчик контента
"""
from anthropic import Anthropic
import re
from typing import Dict


class ContentProcessor:
    """Обработка контента с помощью AI"""
    
    def __init__(self, api_key: str, provider: str = 'claude'):
        self.api_key = api_key
        self.provider = provider
        
        if provider == 'claude':
            self.client = Anthropic(api_key=api_key)
            self.model = "claude-3-5-sonnet-20241022"
    
    async def process_post(self, title: str, description: str, url: str, source: str) -> Dict:
        """
        Обработка поста: рерайтинг, добавление эмодзи, форматирование
        
        Args:
            title: Заголовок
            description: Описание
            url: Ссылка на источник
            source: Источник (github/habr)
        
        Returns:
            Dict с обработанным контентом
        """
        
        # Формируем промпт в зависимости от источника
        if source == 'github':
            prompt = self._create_github_prompt(title, description, url)
        else:
            prompt = self._create_habr_prompt(title, description, url)
        
        # Получаем ответ от AI
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            formatted_text = response.content[0].text
            
            # Конвертируем в Telegram Markdown V2
            formatted_text = self._convert_to_telegram_markdown(formatted_text)
            
            return {
                'title': title,
                'formatted_text': formatted_text,
                'url': url,
                'source': source
            }
            
        except Exception as e:
            print(f"Ошибка AI обработки: {e}")
            # Fallback: простое форматирование без AI
            return self._create_fallback_post(title, description, url, source)
    
    def _create_github_prompt(self, title: str, description: str, url: str) -> str:
        """Промпт для GitHub проекта"""
        return f"""Создай увлекательный пост для Telegram-канала о GitHub проекте.

Название проекта: {title}
Описание: {description}
Ссылка: {url}

Требования:
1. Пост должен быть написан живым, увлекательным языком
2. Добавь 2-3 релевантных эмодзи в начало и по тексту
3. Кратко опиши что делает проект (2-3 предложения)
4. Выдели ключевые особенности
5. Используй Markdown форматирование: **жирный**, *курсив*, `код`
6. Добавь призыв к действию в конце
7. Общая длина: 150-250 слов
8. В конце добавь ссылку: 🔗 [Смотреть на GitHub]({url})

Пиши на русском языке. Будь энергичным и позитивным!"""
    
    def _create_habr_prompt(self, title: str, description: str, url: str) -> str:
        """Промпт для статьи с Habr"""
        return f"""Создай увлекательный пост для Telegram-канала о статье с Habr.

Название: {title}
Описание: {description}
Ссылка: {url}

Требования:
1. Пост должен быть написан живым, увлекательным языком
2. Добавь 2-3 релевантных эмодзи в начало и по тексту
3. Кратко перескажи основную идею статьи (2-3 предложения)
4. Выдели ключевые моменты
5. Используй Markdown форматирование: **жирный**, *курсив*, `код`
6. Добавь призыв к действию в конце
7. Общая длина: 150-250 слов
8. В конце добавь ссылку: 📖 [Читать на Habr]({url})

Пиши на русском языке. Будь информативным и интересным!"""
    
    def _convert_to_telegram_markdown(self, text: str) -> str:
        """
        Конвертация Markdown в Telegram MarkdownV2
        Экранирование специальных символов
        """
        # Специальные символы для экранирования в MarkdownV2
        # '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'
        
        # Сначала защищаем уже имеющееся форматирование
        # Заменяем ** на временные маркеры
        text = text.replace('**', '⟪BOLD⟫')
        text = text.replace('*', '⟪ITALIC⟫')
        text = text.replace('`', '⟪CODE⟫')
        
        # Экранируем специальные символы
        special_chars = ['_', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, '\\' + char)
        
        # Восстанавливаем форматирование
        text = text.replace('⟪BOLD⟫', '*')
        text = text.replace('⟪ITALIC⟫', '_')
        text = text.replace('⟪CODE⟫', '`')
        
        return text
    
    def _create_fallback_post(self, title: str, description: str, url: str, source: str) -> Dict:
        """Fallback форматирование без AI"""
        emoji = "🚀" if source == "github" else "📖"
        
        # Экранируем текст для Telegram
        title_escaped = self._escape_markdown(title)
        desc_escaped = self._escape_markdown(description[:200])
        url_escaped = self._escape_markdown(url)
        
        text = f"""{emoji} *{title_escaped}*

{desc_escaped}

🔗 [Подробнее]({url_escaped})"""
        
        return {
            'title': title,
            'formatted_text': text,
            'url': url,
            'source': source
        }
    
    def _escape_markdown(self, text: str) -> str:
        """Экранирование для Telegram MarkdownV2"""
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, '\\' + char)
        return text
