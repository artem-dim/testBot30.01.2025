from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from imei_service import IMEIService
from utils.imei_validator import validate_imei
from utils.auth import is_user_allowed
import os
import asyncio

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USERS = {int(user_id) for user_id in os.getenv("ALLOWED_USERS", "").split(",")}  # Белый список пользователей

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

imei_service = IMEIService(api_key=os.getenv("IMEI_CHECK_API_KEY"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне IMEI для проверки.")

@dp.message_handler()
async def check_imei(message: types.Message):
    if not is_user_allowed(message.from_user.id, ALLOWED_USERS):
        await message.reply("Доступ запрещен.")
        return

    imei = message.text
    if not validate_imei(imei):
        await message.reply("Некорректный IMEI.")
        return

    try:
        imei_info = await imei_service.check_imei(imei)  # Убедитесь, что check_imei является асинхронным
        await message.reply(f"Информация о IMEI:\n{imei_info.data}")
    except Exception as e:
        await message.reply(f"Ошибка при проверке IMEI: {e}")

async def on_shutdown(dp):
    await bot.close()
    await imei_service.close()  # Закрытие сессии в IMEIService, если это необходимо

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)