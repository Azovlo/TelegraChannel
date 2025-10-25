#!/bin/bash
# Скрипт запуска бота 24/7

cd "$(dirname "$0")"

# Проверяем, не запущен ли уже бот
if pgrep -f "python run.py" > /dev/null; then
    echo "❌ Бот уже запущен!"
    exit 1
fi

# Активируем виртуальное окружение и запускаем бота
source venv/bin/activate
nohup python run.py > bot.log 2>&1 &

echo "✅ Бот запущен в фоновом режиме!"
echo "📋 Для просмотра логов: tail -f bot.log"
echo "🛑 Для остановки: ./stop_bot.sh"
echo "📊 Для проверки статуса: ./status_bot.sh"

