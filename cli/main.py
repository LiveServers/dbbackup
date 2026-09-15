import os
import typer
from utils.load_config import load_config
from utils.precheck import check_binaries, test_connection
from utils.logger import logger
from core.manager import BackupManager
from core.base import StorageTypeConfig
from core.scheduler import start_daily_scheduler

app = typer.Typer()

def run_backup(config: dict, storage_type: StorageTypeConfig, verbose: bool) -> str:
    manager = BackupManager(config, storage_type, verbose=verbose)
    result = manager.run_postgres_backup()
    logger.info(f"Local backup stored at: {result}")
    return result

@app.command()
def backup(
    config: str,
    storage_type: StorageTypeConfig = "local",
    verbose: bool = False,
    schedule: bool = typer.Option(
        False, "--schedule", help="Keep running and backup daily instead of once"
    ),
    at: str = typer.Option("21:00", "--at", help="Daily backup time in HH:MM (24-hour)"),
    timezone: str = typer.Option(
        os.getenv("TZ", "Africa/Nairobi"),
        "--timezone",
        help="IANA timezone for the schedule, e.g. Africa/Nairobi",
    ),
):
    loaded_config = load_config(config)
    check_binaries(loaded_config["db_type"])
    test_connection(loaded_config)

    if not schedule:
        result = run_backup(loaded_config, storage_type, verbose)
        typer.echo(f"Local backup stored at: {result}")
        return

    def scheduled_job():
        try:
            run_backup(loaded_config, storage_type, verbose)
        except Exception:
            logger.exception("Scheduled backup failed")

    start_daily_scheduler(scheduled_job, at=at, timezone=timezone)

if __name__ == "__main__":
    app()
