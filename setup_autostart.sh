#!/bin/bash
# Скрипт настройки автозапуска бота при загрузке системы

cd "$(dirname "$0")"

# Создаем plist файл для launchd (macOS)
cat > ~/Library/LaunchAgents/com.telegram.bot.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.telegram.bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(pwd)/start_bot.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$(pwd)</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$(pwd)/bot.log</string>
    <key>StandardErrorPath</key>
    <string>$(pwd)/bot_error.log</string>
</dict>
</plist>
EOF

echo "✅ Создан файл автозапуска: ~/Library/LaunchAgents/com.telegram.bot.plist"
echo "📋 Для активации автозапуска выполните:"
echo "   launchctl load ~/Library/LaunchAgents/com.telegram.bot.plist"
echo "📋 Для отключения автозапуска:"
echo "   launchctl unload ~/Library/LaunchAgents/com.telegram.bot.plist"

