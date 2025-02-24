from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite:///data/ecommerce.db"
    APP_DB_URL: str = "sqlite:///data/app.db"

    MODEL_ID: str = "gpt-4o"

    class Config:
        env_file = ".env"


settings = Settings()
