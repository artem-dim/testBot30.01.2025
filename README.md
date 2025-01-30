# IMEI Checker

## Описание
Проект для проверки IMEI устройств через Telegram-бота и API.

## Установка
1. Установите зависимости:
   pip install -r requirements.txt

2. Создайте файл .env и добавьте переменные окружения:
    TELEGRAM_BOT_TOKEN=ваш_токен_бота
    IMEI_CHECK_API_KEY=e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b
    ALLOWED_USERS=123456789,987654321  # ID пользователей через запятую
    API_TOKEN=ваш_токен_API

3. Запустите проект:
    python app/main.py

## Использование

Telegram-бот: отправьте IMEI боту для проверки.

API: отправьте POST-запрос на /api/check-imei с параметрами imei и token.