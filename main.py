from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from bot.bot_instance import dp, bot
from bot import bot as bot_handlers
from config import config
import uvicorn
from aiogram.types import Update
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(url=config.WEBHOOK_URL, allowed_updates=dp.resolve_used_update_types(), drop_pending_updates=True)
    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)


logging.basicConfig(level=logging.DEBUG)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)



if __name__ == '__main__':
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT, reload=True)