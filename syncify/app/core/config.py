from datetime import datetime
import pytz
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    google_state: str
    client_id: str
    client_secret: str
    staticfiles: str  # 'syncify/app/static/src'
    facebook_secret: str
    facebook_id: int
    logs_file: str

    sqlalchemy_url: str

    def get_local_time_with_timezone(self):
        tz = pytz.timezone("Africa/Nairobi")
        time = datetime.now(tz=tz)
        return time


settings = Settings(_env_file='syncify/.env')
