from datetime import datetime

import pytz
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = 'Syncify'
    ALGORITHM: str = 'HS256'

    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: int = 1256
    POSTGRES_DATABASE_NAME: str = 'sync'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1400
    SECRET_KEY: str = 'cnmxcgxnzcbxzzxsgdsfjshdcjdfnvdfkvbzxd.kgui'

    sqlalchemy_url: str = 'postgresql://postgres:1256@localhost/sync'

    def get_local_time_with_timezone(self):
        tz = pytz.timezone("Africa/Nairobi")
        time = datetime.now(tz=tz)
        return time


settings = Settings()
