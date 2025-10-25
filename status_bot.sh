#!/bin/bash
# Скрипт проверки статуса бота

cd "$(dirname "$0")"

PID=$(pgrep -f "python run.py")
if [ -n "$PID" ]; then
    echo "✅ Бот работает (PID: $PID)"
    echo "📋 Последние логи:"
    tail -10 bot.log
else
    echo "❌ Бот не запущен"
fi

