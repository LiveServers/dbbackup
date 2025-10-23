from .base import BaseDbBackup
from datetime import datetime as dt
from utils.logger import logger
import subprocess
import os

class PostgresBackup(BaseDbBackup):
    def __init__(self, db_host: str, db_username:str, db_password:str, db_port:str, db_name:str, db_type:str, output_path: str) -> None:
        self.db_host = db_host
        self.db_username = db_username
        self.db_password = db_password
        self.db_port = db_port
        self.db_name = db_name
        self.db_type = db_type
        self.output_path = output_path

    def backup(self, backup_type:str = "full", compression: bool = False) -> str:
        try:
            timestamp = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
            dump_path = os.path.join(
            self.output_path,
            f"{self.db_name}-{timestamp}_backup.dump"
        )
            dump_cmd = [
                "pg_dump",
                "-h", self.db_host,
                "-p", str(self.db_port),
                "-U", self.db_username,
                "-F", "c",
                "-f", dump_path,
                self.db_name
            ]
            subprocess.run(dump_cmd, check=True)
            return dump_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to connect to {self.db_type}: {e.stderr.decode()}")
            raise