from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PGHOST: str
    PGDATABASE: str
    PGUSER: str
    PGPASSWORD: str
    PGSSLMODE: str
    PGCHANNELBINDING: str

    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()
