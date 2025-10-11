# parsers/habr_parser.py
"""
Парсер Habr
"""
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
from fake_useragent import UserAgent


class HabrParser:
    """Парсер для Habr"""
    
    BASE_URL = "https://habr.com/ru/flows/develop/articles"
    
    def __init__(self):
        self.ua = UserAgent()
    
    async def fetch_articles(self, period: str = 'daily', limit: int = 10) -> List[Dict]:
        """
        Получение лучших статей с Habr
        
        Args:
            period: Период (daily, weekly, monthly, yearly, alltime)
            limit: Максимальное количество статей
        """
        # Формируем URL в зависимости от периода
        if period == 'daily':
            url = f"{self.BASE_URL}/top/daily/"
        elif period == 'weekly':
            url = f"{self.BASE_URL}/top/weekly/"
        elif period == 'monthly':
            url = f"{self.BASE_URL}/top/monthly/"
        else:
            url = f"{self.BASE_URL}/"
        
        headers = {'User-Agent': self.ua.random}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        return []
                    
                    html = await response.text()
                    return self._parse_html(html, limit)
        except Exception as e:
            print(f"Ошибка при парсинге Habr: {e}")
            return []
    
    def _parse_html(self, html: str, limit: int) -> List[Dict]:
        """Парсинг HTML страницы Habr"""
        soup = BeautifulSoup(html, 'lxml')
        articles_tags = soup.find_all('article', class_='tm-articles-list__item')
        
        articles = []
        for article_tag in articles_tags[:limit]:
            try:
                # Заголовок и URL
                title_tag = article_tag.find('h2', class_='tm-title')
                if not title_tag:
                    continue
                
                link = title_tag.find('a')
                if not link:
                    continue
                
                title = link.text.strip()
                url = 'https://habr.com' + link['href']
                
                # Описание (превью)
                desc_tag = article_tag.find('div', class_='article-formatted-body')
                description = ''
                if desc_tag:
                    description = desc_tag.text.strip()[:300] + '...'
                
                # Просмотры
                views_tag = article_tag.find('span', class_='tm-icon-counter__value')
                views = 0
                if views_tag:
                    views_text = views_tag.text.strip().replace('K', '000').replace(',', '')
                    try:
                        views = int(float(views_text))
                    except:
                        pass
                
                # Рейтинг
                rating_tag = article_tag.find('span', class_='tm-votes-meter__value')
                rating = 0
                if rating_tag:
                    try:
                        rating = int(rating_tag.text.strip())
                    except:
                        pass
                
                # Теги
                tags = []
                tags_container = article_tag.find('div', class_='tm-article-snippet__hubs')
                if tags_container:
                    tag_links = tags_container.find_all('a')
                    tags = [tag.text.strip() for tag in tag_links]
                
                articles.append({
                    'title': title,
                    'description': description,
                    'url': url,
                    'views': views,
                    'rating': rating,
                    'tags': tags,
                    'source': 'habr'
                })
                
            except Exception as e:
                print(f"Ошибка парсинга статьи: {e}")
                continue
        
        return articles
