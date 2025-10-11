# parsers/github_parser.py
"""
Парсер GitHub Trending
"""
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
from fake_useragent import UserAgent


class GitHubParser:
    """Парсер для GitHub Trending"""
    
    BASE_URL = "https://github.com/trending"
    
    def __init__(self):
        self.ua = UserAgent()
    
    async def fetch_trending(self, language: str = 'python', period: str = 'daily') -> List[Dict]:
        """
        Получение трендовых проектов с GitHub
        
        Args:
            language: Язык программирования (python, javascript, all и т.д.)
            period: Период (daily, weekly, monthly)
        """
        url = f"{self.BASE_URL}/{language}?since={period}"
        headers = {'User-Agent': self.ua.random}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        return []
                    
                    html = await response.text()
                    return self._parse_html(html)
        except Exception as e:
            print(f"Ошибка при парсинге GitHub: {e}")
            return []
    
    def _parse_html(self, html: str) -> List[Dict]:
        """Парсинг HTML страницы GitHub Trending"""
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all('article', class_='Box-row')
        
        projects = []
        for article in articles:
            try:
                # Название и URL
                h2 = article.find('h2')
                if not h2:
                    continue
                
                link = h2.find('a')
                if not link:
                    continue
                
                repo_path = link['href'].strip()
                repo_name = repo_path.lstrip('/')
                url = f"https://github.com{repo_path}"
                
                # Описание
                desc_tag = article.find('p', class_='col-9')
                description = desc_tag.text.strip() if desc_tag else ''
                
                # Звезды
                stars_tag = article.find('svg', class_='octicon-star')
                stars = 0
                if stars_tag:
                    parent = stars_tag.parent
                    stars_text = parent.text.strip().replace(',', '')
                    try:
                        stars = int(stars_text)
                    except:
                        pass
                
                # Звезды сегодня
                stars_today_tag = article.find('span', class_='d-inline-block float-sm-right')
                stars_today = 0
                if stars_today_tag:
                    stars_today_text = stars_today_tag.text.strip().split()[0].replace(',', '')
                    try:
                        stars_today = int(stars_today_text)
                    except:
                        pass
                
                # Язык программирования
                lang_tag = article.find('span', itemprop='programmingLanguage')
                language = lang_tag.text.strip() if lang_tag else 'Unknown'
                
                projects.append({
                    'title': repo_name,
                    'description': description,
                    'url': url,
                    'stars': stars,
                    'stars_today': stars_today,
                    'language': language,
                    'source': 'github'
                })
                
            except Exception as e:
                print(f"Ошибка парсинга проекта: {e}")
                continue
        
        return projects
