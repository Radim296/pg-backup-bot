import os
import subprocess
from typing import Dict
from aiogram.types import BufferedInputFile
import datetime
import asyncpg
import psycopg2

from app.config import DBConfiguration


async def is_postgresql_db_alive(db_config: DBConfiguration):
    try:
        # Attempt to create a connection to the PostgreSQL database
        connection = await asyncpg.connect(
            user=db_config.USER,
            password=db_config.PASSWORD,
            host=db_config.HOST,
            port=db_config.PORT,
            database=db_config.NAME,
        )
        await connection.execute("SELECT version();")
        print(
            f"Successfully connected to {db_config.NAME} on {db_config.HOST}:{db_config.PORT}"
        )
        return True
    except Exception as e:
        print(f"Error: '{e}' occurred.")
        return False
    finally:
        if "connection" in locals():
            await connection.close()


async def get_database_backup(db_config: DBConfiguration) -> bytes:
    """
    The function `backup_db` creates a database backup file using pg_dump, sends it to a chat using a
    Telegram bot, and then deletes the backup file.
    """
    backup_filename: str = (
        f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    )
    backup_path: str = os.path.join("/tmp", backup_filename)

    # Execute pg_dump command
    command: str = f"pg_dump -h {db_config.HOST} -U {db_config.USER} -w {db_config.NAME} -p {db_config.PORT} > {backup_path}"
    env: Dict[str, str] = os.environ.copy()
    env["PGPASSWORD"] = db_config.PASSWORD
    subprocess.run(command, shell=True, env=env, check=True)

    backup_bytes: bytes = open(backup_path).read().encode()

    # Clean up after sending
    os.remove(backup_path)

    return backup_bytes
