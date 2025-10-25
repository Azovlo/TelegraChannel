#!/bin/bash
# Скрипт остановки бота

cd "$(dirname "$0")"

# Находим и останавливаем процесс бота
PID=$(pgrep -f "python run.py")
if [ -n "$PID" ]; then
    kill $PID
    echo "✅ Бот остановлен (PID: $PID)"
else
    echo "❌ Бот не запущен"
fi

