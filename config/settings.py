from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_PUBLIC_TOKEN: str
    TELEGRAM_ADMIN_TOKEN: str
    ADMIN_TELEGRAM_ID: int

    DATABASE_URL: str
    REDIS_URL: str = None

    MERCADOPAGO_ACCESS_TOKEN: str
    MERCADOPAGO_WEBHOOK_URL: str

    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"

    ENV: str = "development"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
