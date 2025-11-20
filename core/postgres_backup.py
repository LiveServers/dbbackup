from .base import BaseDbBackup
from utils.logger import logger
import subprocess

class PostgresBackup(BaseDbBackup):
    def __init__(self, db_host: str, db_username:str, db_password:str, db_port:str, db_name:str, db_type:str, output_path: str) -> None:
        self.db_host = db_host
        self.db_username = db_username
        self.db_password = db_password
        self.db_port = db_port
        self.db_name = db_name
        self.db_type = db_type
        self.output_path = output_path

    def backup(self, dump_path: str, backup_type:str = "full", compression: bool = False, verbose: bool = False):
        try:
            dump_cmd = [
                "pg_dump",
                "-h", self.db_host,
                "-p", str(self.db_port),
                "-U", self.db_username,
                "-F", "c",
                "-f", dump_path,
            ]

            # env = os.environ.copy()
            # env['PGPASSWORD'] = self.db_password

            if verbose:
                dump_cmd.append("-v")

            dump_cmd.append(self.db_name)

            process = subprocess.Popen(dump_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, env=env)

            for line in process.stderr:
                clean = line.rstrip("\n")
                if verbose:
                    yield clean

            process.wait()

            if int(process.returncode) != 0:
                error = process.stderr.read()
                logger.error(f"Failed to backup your database due to {error}")
                raise RuntimeError(f"Backup failed: {error}")
            
            yield "Backup completed successfully"
        except Exception as e:
            logger.error(f"Failed to backup {self.db_name}: {e}")
            raise