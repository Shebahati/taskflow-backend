from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # JWT
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_SECONDS: int = 60 * 60  # 1 hour

    # DB
    DATABASE_URL: str

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "console"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
