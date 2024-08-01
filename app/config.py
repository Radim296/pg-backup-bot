import os
from typing import Optional, Union
import datetime

from dotenv import find_dotenv, load_dotenv

load_dotenv(dotenv_path=find_dotenv())


class DBConfiguration:
    NAME: str = os.getenv("POSTGRES_DB")
    USER: str = os.getenv("POSTGRES_USER")
    PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    HOST: str = os.getenv("POSTGRES_HOST")
    PORT: int = os.getenv("POSTGRES_PORT")

    def __init__(self) -> None:
        if not all([self.NAME, self.USER, self.PASSWORD, self.HOST, self.PORT]):
            raise ValueError("Invalid database configuration")


class TelegramConfiguration:
    BOT_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID: Union[str, int] = os.getenv("CHAT_ID")
    MESSAGE_THREAD_ID: Optional[int] = os.getenv("MESSAGE_THREAD_ID")
    LOGGING: bool = bool(os.getenv("LOGGING", 0))
    def __init__(self) -> None:
        if not all([self.BOT_TOKEN, self.CHAT_ID]):
            raise ValueError("Invalid telegram configuration")


class SchedulerConfiguration:
    TIME_TO_SEND: Optional[datetime.time] = os.getenv("TIME_TO_SEND")
    INTERVAL: Optional[str] = os.getenv("INTERVAL")
    JOB_NAME: str = "db_backup_job_name"
    JOB_ID: str = "db_backup_job_id"
    TASK_DATABASE_PATH: str = "sqlite:///jobs.sqlite"


class Configuration:
    db: DBConfiguration = DBConfiguration()
    telegram: TelegramConfiguration = TelegramConfiguration()
    scheduler: SchedulerConfiguration = SchedulerConfiguration()
