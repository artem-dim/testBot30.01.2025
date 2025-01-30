import multiprocessing
from bot import dp
from api import app
import uvicorn
import asyncio
import os

def run_bot():
    asyncio.run(dp.start_polling())

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Запуск бота в отдельном процессе
    bot_process = multiprocessing.Process(target=run_bot)
    bot_process.start()

    # Запуск FastAPI в основном процессе
    run_api()

    # Ожидание завершения процессов (на практике это не произойдет, так как сервер работает бесконечно)
    bot_process.join()
