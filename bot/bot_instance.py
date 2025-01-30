from aiogram import Bot, Dispatcher
from config import config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()