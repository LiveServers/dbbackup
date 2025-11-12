from .postgres_backup import PostgresBackup
from storage.local_storage import LocalStorage
from storage.s3_storage import S3Storage
from typing import cast
from .base import ConfigType, BackupTypeConfig, S3Config, PostgresConfig, StorageTypeConfig, POSTGRES_FIELDS, S3_FIELDS

class BackupManager:
    def __init__(self, config: ConfigType, storage_type: StorageTypeConfig = "local", backup_type: BackupTypeConfig = "full", compression: bool = False):
        self.config = config
        self.backup_type = backup_type
        self.compression = compression
        self.storage_type = storage_type
    
    def __local_storage(self, backup_file: str) -> str:
        local_storage = LocalStorage()
        data_dump_storage = local_storage.save_backup(backup_file, "local_storage")
        return data_dump_storage

    def __s3_storage(self, backup_file: str) -> bool:
        s3_config = {k: v for k,v in self.config.items() if k in S3_FIELDS}
        typed_s3_config = cast(S3Config, s3_config)
        s3_storage = S3Storage(**typed_s3_config)
        s3_storage.upload_to_s3(backup_file)
        return True
    
    def select_storage_from_config(self, storage_type: str, backup_file: str):
        match storage_type:
            case "local":
                return self.__local_storage(backup_file)
            case "s3":
                return self.__s3_storage(backup_file)
            case _:
                return f"Unknown storage type {storage_type}"

    def run_postgres_backup(self):
        postgres_config = {k: v for k,v in self.config.items() if k in POSTGRES_FIELDS}
        typed_postgres_config = cast(PostgresConfig, postgres_config)
        backup = PostgresBackup(**typed_postgres_config)
        backup_file = backup.backup()
        response = self.select_storage_from_config(self.storage_type, backup_file)
        return response
    
        
