from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite:///data/ecommerce.db"
    APP_DB_URL: str = "sqlite:///data/app.db"
    OAUTH_SECRET_KEY: str
    GOOGLE_CLIENT_ID: str | None = None

    MODEL_ID: str = "gpt-4o"

    class Config:
        env_file = ".env"


settings = Settings()
