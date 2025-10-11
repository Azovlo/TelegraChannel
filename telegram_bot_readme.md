# 🤖 Telegram Channel Automation Bot

Автоматизированная система для ведения Telegram-канала с парсингом GitHub Trending и Habr.

## 📋 Возможности

- ✅ **Автоматический парсинг** GitHub Trending и Habr
- ✅ **AI-обработка контента** с использованием Claude/OpenAI
- ✅ **Умное форматирование** с эмодзи и Markdown
- ✅ **База данных** для отслеживания публикаций
- ✅ **Гибкая настройка** через переменные окружения
- ✅ **Два режима работы**: одноразовый запуск и непрерывная работа

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Клонируйте репозиторий
git clone <your-repo-url>
cd telegram_channel_bot

# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Создание Telegram бота

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Создайте нового бота командой `/newbot`
3. Следуйте инструкциям и получите токен бота
4. Добавьте бота в ваш канал как администратора

### 3. Получение ID канала

```bash
# Отправьте любое сообщение в канал
# Затем перейдите по ссылке (замените YOUR_BOT_TOKEN):
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates

# Найдите "chat":{"id": -1001234567890} - это ID вашего канала
```

### 4. Получение AI API ключа

**Для Claude (рекомендуется):**
1. Зарегистрируйтесь на [console.anthropic.com](https://console.anthropic.com)
2. Создайте API ключ
3. Используйте модель: `claude-sonnet-4-20250514`

**Для OpenAI (альтернатива):**
1. Зарегистрируйтесь на [platform.openai.com](https://platform.openai.com)
2. Создайте API ключ

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Telegram настройки
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CHANNEL_ID=@your_channel

# AI API ключ
AI_API_KEY=sk-ant-api03-xxx...
AI_PROVIDER=claude

# Источники контента
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

# Режим работы
RUN_MODE=continuous
```

### 6. Запуск бота

```bash
# Одноразовый запуск (для тестирования)
python main.py

# Или измените RUN_MODE=continuous в .env для непрерывной работы
python main.py
```

## 📖 Подробная настройка

### Параметры конфигурации

| Параметр | Описание | Значение по умолчанию |
|----------|----------|----------------------|
| `TELEGRAM_BOT_TOKEN` | Токен бота от BotFather | - |
| `CHANNEL_ID` | ID канала или @username | - |
| `AI_API_KEY` | API ключ Claude/OpenAI | - |
| `AI_PROVIDER` | Провайдер AI (claude/openai) | claude |
| `GITHUB_ENABLED` | Включить парсинг GitHub | true |
| `HABR_ENABLED` | Включить парсинг Habr | true |
| `GITHUB_LANGUAGE` | Язык для GitHub (python, javascript, all) | python |
| `GITHUB_PERIOD` | Период для GitHub (daily, weekly, monthly) | daily |
| `HABR_PERIOD` | Период для Habr (daily, weekly, monthly) | daily |
| `HABR_LIMIT` | Максимум статей с Habr | 10 |
| `POSTS_PER_CYCLE` | Постов за один цикл | 3 |
| `DELAY_BETWEEN_POSTS` | Задержка между постами (сек) | 300 |
| `POSTING_INTERVAL_HOURS` | Интервал между циклами (часы) | 6 |
| `RUN_MODE` | Режим работы (once/continuous) | continuous |

### Режимы работы

**Once (одноразовый):**
```env
RUN_MODE=once
```
Бот запустится один раз, опубликует посты и завершит работу.

**Continuous (непрерывный):**
```env
RUN_MODE=continuous
```
Бот будет работать постоянно, публикуя посты с заданным интервалом.

## 🐳 Запуск в Docker

Создайте `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Создайте `docker-compose.yml`:

```yaml
version: '3.8'

services:
  bot:
    build: .
    env_file:
      - .env
    volumes:
      - ./bot_data.db:/app/bot_data.db
    restart: unless-stopped
```

Запуск:

```bash
docker-compose up -d
```

## 📊 Мониторинг и логи

Бот выводит подробные логи в консоль:

```bash
# Просмотр логов в реальном времени
tail -f bot.log

# С Docker
docker-compose logs -f bot
```

## 🔧 Расширение функционала

### Добавление нового парсера

1. Создайте файл в `parsers/`:

```python
# parsers/your_parser.py
class YourParser:
    async def fetch_content(self):
        # Ваша логика парсинга
        return []
```

2. Добавьте в `main.py`:

```python
from parsers.your_parser import YourParser

# В __init__:
self.your_parser = YourParser()

# В collect_content:
your_items = await self.your_parser.fetch_content()
content_items.extend(your_items)
```

### Изменение AI промптов

Отредактируйте методы в `ai/content_processor.py`:
- `_create_github_prompt()` - для GitHub постов
- `_create_habr_prompt()` - для Habr постов

## 🛠️ Troubleshooting

### Ошибка "Unauthorized"
- Проверьте правильность токена бота
- Убедитесь, что бот добавлен в канал

### Ошибка "Chat not found"
- Проверьте правильность CHANNEL_ID
- Убедитесь, что бот является администратором канала

### Ошибка парсинга
- Проверьте доступность GitHub и Habr
- Возможно, изменилась структура сайта (обновите парсеры)

### AI не отвечает
- Проверьте правильность AI_API_KEY
- Убедитесь, что есть средства на аккаунте
- Проверьте лимиты API

## 📝 Лицензия

MIT License

## 🤝 Поддержка

При возникновении вопросов создайте Issue в репозитории.

## 🎯 Roadmap

- [ ] Поддержка Reddit
- [ ] Веб-интерфейс для управления
- [ ] Аналитика и статистика
- [ ] Планировщик публикаций
- [ ] Множественные каналы
- [ ] Telegram-команды для управления ботом
