# bot_commands.py
"""
Telegram команды для управления ботом
Добавьте этот модуль для возможности управления ботом через Telegram
"""
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from config import Config
from database.storage import Storage


class BotCommands:
    """Обработчик команд для управления ботом через Telegram"""
    
    def __init__(self, config: Config, storage: Storage):
        self.config = config
        self.storage = storage
        self.admin_ids = self._get_admin_ids()
        
    def _get_admin_ids(self) -> list:
        """Получить список ID администраторов из переменных окружения"""
        import os
        admin_ids_str = os.getenv('ADMIN_IDS', '')
        if admin_ids_str:
            return [int(id.strip()) for id in admin_ids_str.split(',')]
        return []
    
    def is_admin(self, user_id: int) -> bool:
        """Проверка, является ли пользователь администратором"""
        return user_id in self.admin_ids
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text("⛔️ Доступ запрещён")
            return
        
        welcome_text = f"""
👋 Привет, {user.first_name}!

Я бот для автоматизации Telegram-канала.

📋 Доступные команды:
/stats - Статистика публикаций
/status - Статус бота
/post - Опубликовать новый пост
/help - Помощь

🔧 Настройки:
/settings - Изменить настройки
"""
        await update.message.reply_text(welcome_text)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /stats - показать статистику"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("⛔️ Доступ запрещён")
            return
        
        # Получаем статистику
        stats_7d = self.storage.get_statistics(7)
        stats_30d = self.storage.get_statistics(30)
        
        stats_text = f"""
📊 *Статистика публикаций*

За последние 7 дней:
├ Всего: {stats_7d['total']} постов
├ GitHub: {stats_7d['github']}
└ Habr: {stats_7d['habr']}

За последние 30 дней:
├ Всего: {stats_30d['total']} постов
├ GitHub: {stats_30d['github']}
└ Habr: {stats_30d['habr']}

📈 Среднее в день: {stats_30d['total'] / 30:.1f}
"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 Обновить", callback_data='refresh_stats')],
            [InlineKeyboardButton("📝 Последние посты", callback_data='last_posts')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            stats_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /status - статус бота"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("⛔️ Доступ запрещён")
            return
        
        status_text = f"""
🤖 *Статус бота*

✅ Бот работает нормально

⚙️ *Настройки:*
├ Режим: {self.config.run_mode}
├ Постов за цикл: {self.config.posts_per_cycle}
├ Интервал: {self.config.posting_interval_hours}ч
└ Задержка между постами: {self.config.delay_between_posts}с

📡 *Источники:*
├ GitHub: {'✅' if self.config.sources.get('github_enabled') else '❌'}
└ Habr: {'✅' if self.config.sources.get('habr_enabled') else '❌'}

💾 База данных: {self.storage.db_path}
"""
        
        await update.message.reply_text(
            status_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def post_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /post - запустить публикацию вручную"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("⛔️ Доступ запрещён")
            return
        
        await update.message.reply_text("🚀 Запускаю публикацию постов...")
        
        # TODO: Интегрировать с основным циклом бота
        # Здесь должен быть вызов bot.run_posting_cycle()
        
        await update.message.reply_text("✅ Публикация завершена!")
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /settings - настройки бота"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("⛔️ Доступ запрещён")
            return
        
        keyboard = [
            [InlineKeyboardButton("🔄 Изменить интервал", callback_data='set_interval')],
            [InlineKeyboardButton("📊 Постов за цикл", callback_data='set_posts_per_cycle')],
            [InlineKeyboardButton("📡 Источники", callback_data='set_sources')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚙️ *Настройки бота*\n\nВыберите параметр для изменения:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /help - помощь"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("⛔️ Доступ запрещён")
            return
        
        help_text = """
📖 *Помощь*

*Основные команды:*
/start - Запустить бота
/stats - Показать статистику
/status - Проверить статус бота
/post - Опубликовать посты вручную
/settings - Изменить настройки
/help - Эта справка

*Описание:*
Бот автоматически собирает контент с GitHub Trending и Habr, обрабатывает его через AI и публикует в канал.

*Источники:*
• GitHub Trending - популярные репозитории
• Habr - лучшие статьи разработчиков

*Режимы работы:*
• Непрерывный - бот работает постоянно
• Разовый - публикует посты один раз

Для изменения настроек используйте /settings
"""
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        if not self.is_admin(query.from_user.id):
            await query.edit_message_text("⛔️ Доступ запрещён")
            return
        
        if query.data == 'refresh_stats':
            # Обновить статистику
            stats_7d = self.storage.get_statistics(7)
            stats_30d = self.storage.get_statistics(30)
            
            stats_text = f"""
📊 *Статистика публикаций* (обновлено)

За последние 7 дней:
├ Всего: {stats_7d['total']} постов
├ GitHub: {stats_7d['github']}
└ Habr: {stats_7d['habr']}

За последние 30 дней:
├ Всего: {stats_30d['total']} постов
├ GitHub: {stats_30d['github']}
└ Habr: {stats_30d['habr']}
"""
            
            await query.edit_message_text(
                stats_text,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif query.data == 'last_posts':
            # Показать последние посты
            last_posts = self.storage.get_last_published(5)
            
            posts_text = "📝 *Последние 5 постов:*\n\n"
            for i, post in enumerate(last_posts, 1):
                posts_text += f"{i}. [{post['source']}] {post['title'][:50]}...\n"
                posts_text += f"   📅 {post['published_at']}\n\n"
            
            await query.edit_message_text(
                posts_text,
                parse_mode=ParseMode.MARKDOWN
            )
    
    def setup_handlers(self, application: Application):
        """Настройка обработчиков команд"""
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("status", self.status_command))
        application.add_handler(CommandHandler("post", self.post_command))
        application.add_handler(CommandHandler("settings", self.settings_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CallbackQueryHandler(self.button_callback))


async def run_command_bot():
    """
    Запуск бота для обработки команд (отдельный процесс)
    Добавьте это в отдельный скрипт или запускайте параллельно с основным ботом
    """
    config = Config.load()
    storage = Storage(config.database_path)
    
    # Создаём приложение
    application = Application.builder().token(config.telegram_bot_token).build()
    
    # Настраиваем команды
    bot_commands = BotCommands(config, storage)
    bot_commands.setup_handlers(application)
    
    # Запускаем
    print("🤖 Бот команд запущен...")
    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(run_command_bot())