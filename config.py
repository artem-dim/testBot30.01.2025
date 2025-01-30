from os.path import join, dirname
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Config(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "defaulbottoken")
    API_TOKEN: str = os.getenv("API_TOKEN")
    WHITE_LIST: list[int] = [1310527408]  # ID разрешённых пользователей

    APP_HOST: str = 'localhost'
    APP_PORT: int = 8000


    WEBHOOK_URL: str = 'https://65b5-94-158-60-140.ngrok-free.app/webhook'
    WEBHOOK_PATH: str = '/webhook'

    URL_CHECK: str = "https://api.imeicheck.net/v1/checks"
    SERVICE_ID: int = 12

    model_config = SettingsConfigDict(
        env_file=join(dirname(__file__), '.env'),
        env_file_encoding='utf-8'
    )

config = Config()