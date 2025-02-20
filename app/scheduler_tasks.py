import datetime
from aiogram import Bot
from aiogram.types import BufferedInputFile

from app.archiver import make_archive
from app.config import Configuration
from app.db import get_database_backup
from app.message_functions import check_database_connection


async def send_db_backup(config: Configuration):
    bot: Bot = Bot(token=config.telegram.BOT_TOKEN)

    await check_database_connection(config=config, bot=bot)

    try:
        backup_bytes: bytes = await get_database_backup(
            db_config=config.db
        )

        backup_bytes: bytes = make_archive(
            data=backup_bytes,
            config=config
        )

        await bot.send_document(
            document=BufferedInputFile(file=backup_bytes, filename="backup.sql"),
            chat_id=config.telegram.CHAT_ID,
            message_thread_id=config.telegram.MESSAGE_THREAD_ID,
            caption=f"💿 Backup - {datetime.datetime.now()}"
        )
    except Exception as exc:
        await bot.send_message(
            text=f"❌ Failed to load backup - {exc}"[:4000],
            chat_id=config.telegram.CHAT_ID,
            message_thread_id=config.telegram.MESSAGE_THREAD_ID
        )
    finally:
        await bot.session.close()
