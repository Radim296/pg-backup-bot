import os
from typing import Optional, Union
import datetime

from dotenv import find_dotenv, load_dotenv

load_dotenv(dotenv_path=find_dotenv(raise_error_if_not_found=True))

class DBConfiguration:
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")

    def __init__(self) -> None:
        if not all(
            [self.DB_NAME, self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT]
        ):
            raise ValueError("Invalid database configuration")


class TelegramConfiguration:
    BOT_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID: Union[str, int] = os.getenv("CHAT_ID")
    MESSAGE_THREAD_ID: Optional[int] = os.getenv("MESSAGE_THREAD_ID")

    def __init__(self) -> None:
        if not all([self.BOT_TOKEN, self.CHAT_ID]):
            raise ValueError("Invalid telegram configuration")


class SchedulerConfiguration:
    TIME_TO_SEND: datetime.time = datetime.datetime.strptime(
        os.getenv("TIME_TO_SEND") or "00:00", "%H:%M"
    ).time()
    JOB_NAME: str = "db_backup_job_name"
    JOB_ID: str = "db_backup_job_id"
    TASK_DATABASE_PATH: str = "sqlite:///jobs.sqlite"


class Configuration:
    db: DBConfiguration = DBConfiguration()
    telegram: TelegramConfiguration = TelegramConfiguration()
    scheduler: SchedulerConfiguration = SchedulerConfiguration()
