from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PGHOST: str
    PGDATABASE: str
    PGUSER: str
    PGPASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
