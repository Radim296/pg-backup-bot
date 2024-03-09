from configparser import ConfigParser
import math
import time

from aiogram import Bot

from app.config import Configuration
from app.db import is_postgresql_db_alive


async def check_database_connection(config: Configuration, bot: Bot) -> bool:
    tries: int = 0

    while not await is_postgresql_db_alive(db_config=config.db):
        tries += 1
        delay_time: float = math.ceil(10 / tries)
        await bot.send_message(
            chat_id=config.telegram.CHAT_ID,
            message_thread_id=config.telegram.MESSAGE_THREAD_ID,
            text=f"⚠️ The database is not accessable {tries} (next try after {delay_time} seconds)",
        )
        time.sleep(delay_time)

    return True
