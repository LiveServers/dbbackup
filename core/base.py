from abc import ABC, abstractmethod
from typing import Literal, TypedDict, Union, Optional

class BaseDbBackup(ABC):
    # @abstractmethod
    # def test_connection(self):
    #     pass

    @abstractmethod
    def backup(self):
        pass

    # @abstractmethod
    # def restore(self):
    #     pass

StorageTypeConfig = Literal["local", "s3"]
BackupTypeConfig = Literal["full", "incremental", "differential"]

class BaseConfig(TypedDict):
    db_type: str
    output_path: str

class PostgresConfig(BaseConfig):
    db_name: str
    db_host: str
    db_port: str
    db_username: str
    db_password: str

class S3Config(TypedDict):
    bucket_name: str
    region: str
    access_key_id: str
    secret_access_key: str

ConfigType = Union[PostgresConfig, S3Config]

POSTGRES_FIELDS = {
    "db_name", "db_host", "db_port",
    "db_username", "db_password", "db_type", "output_path"
}

S3_FIELDS = {
    "bucket_name", "region", "access_key_id", "secret_access_key"
}