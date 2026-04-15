from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool
    HOST: str
    PORT: int

    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int
    REFRESH_EXPIRE_DAYS: int

    class Config:
        env_file = ".env"


settings = Settings()
