from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.logger import logger


def parse_daily_time(at: str) -> tuple[int, int]:
    try:
        hour_str, minute_str = at.strip().split(":")
        hour = int(hour_str)
        minute = int(minute_str)
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError
        return hour, minute
    except ValueError as exc:
        raise ValueError("Time must be HH:MM in 24-hour format, e.g. 21:00") from exc


def start_daily_scheduler(job, at: str, timezone: str) -> None:
    hour, minute = parse_daily_time(at)
    tz = ZoneInfo(timezone)
    scheduler = BlockingScheduler(timezone=tz)
    trigger = CronTrigger(hour=hour, minute=minute, timezone=tz)
    scheduler.add_job(
        job,
        trigger,
        id="daily_backup",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=3600,
    )
    next_run = trigger.get_next_fire_time(None, datetime.now(tz))
    logger.info(
        f"Daily backup scheduled at {hour:02d}:{minute:02d} {timezone}. Next run: {next_run}"
    )
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")
