from .postgres_backup import PostgresBackup
from utils.logger import logger
from storage.local_storage import LocalStorage
from typing import TypedDict, Literal

BackupType = Literal["full", "incremental", "differential"]

class ConfigType(TypedDict):
    db_name: str
    db_host: str
    db_port: str
    db_username: str
    db_password: str
    db_type: str
    output_path: str

class BackupManager:
    def __init__(self, config: ConfigType, backup_type: BackupType = "full", compression: bool = False):
        self.config = config
        self.backup_type = backup_type
        self.compression = compression

    def run_postgres_backup(self):
        backup = PostgresBackup(**self.config)
        backup_file = backup.backup()
        print("BACKUP FILE", backup_file)
        local_storage = LocalStorage()
        data_dump_storage = local_storage.save_backup(backup_file, "local_storage")
        return data_dump_storage
        
