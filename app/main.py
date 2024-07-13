import asyncio
import datetime
import logging
from operator import le
from typing import Optional, Union

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.job import Job

from app.config import Configuration
from app.message_functions import check_database_connection
from app.scheduler_tasks import send_db_backup


def get_scheduler(config: Configuration) -> AsyncIOScheduler:
    """
    The function `get_scheduler` returns an instance of `AsyncIOScheduler` with a job store and executor
    added.
    :return: an instance of the `AsyncIOScheduler` class.
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_jobstore(SQLAlchemyJobStore(url=config.scheduler.TASK_DATABASE_PATH))
    scheduler.add_executor(AsyncIOExecutor())

    scheduler.start()

    return scheduler


def get_scheduler_trigger(config: Configuration) -> Union[CronTrigger, IntervalTrigger]:
    if config.scheduler.INTERVAL:
        if config.scheduler.INTERVAL.isdigit():
            return IntervalTrigger(
                minutes=int(config.scheduler.INTERVAL),
                start_date=datetime.datetime.now(),
            )
    elif config.scheduler.TIME_TO_SEND:
        return CronTrigger(
            hour=config.scheduler.TIME_TO_SEND.hour,
            minute=config.scheduler.TIME_TO_SEND.minute,
            start_date=datetime.datetime.now(),
        )
    else:
        return CronTrigger(
            hour=0,
            minute=0,
            start_date=datetime.datetime.now(),
        )


def schedule_jobs(scheduler: AsyncIOScheduler, config: Configuration) -> None:
    job: Optional[Job] = scheduler.get_job(config.scheduler.JOB_ID)

    if job:
        job.remove()

    scheduler.add_job(
        send_db_backup,
        kwargs={"config": config},
        trigger=get_scheduler_trigger(config=config),
        name=config.scheduler.JOB_NAME,
        id=config.scheduler.JOB_ID,
    )


async def start_bot():
    logging.basicConfig(level=logging.DEBUG)
    config: Configuration = Configuration()
    scheduler: AsyncIOScheduler = get_scheduler(config=config)
    bot: Bot = Bot(token=config.telegram.BOT_TOKEN, parse_mode=ParseMode.HTML)

    await bot.send_message(
        chat_id=config.telegram.CHAT_ID,
        message_thread_id=config.telegram.MESSAGE_THREAD_ID,
        text=f"👨‍🔧 <b>Backup Service Started </b>({datetime.datetime.now().isoformat()})",
    )

    await check_database_connection(config=config, bot=bot)
    schedule_jobs(scheduler=scheduler, config=config)

    await bot.session.close()

    while True:
        await asyncio.sleep(1)
