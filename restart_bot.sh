#!/bin/bash
# Скрипт перезапуска бота

cd "$(dirname "$0")"

echo "🔄 Перезапуск бота..."
./stop_bot.sh
sleep 2
./start_bot.sh

