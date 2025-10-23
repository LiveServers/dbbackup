import shutil
import subprocess
from .logger import logger

REQUIRED_BINARIES = {
    "postgres": ["pg_dump", "pg_restore"],
    "mysql": ["mysqldump", "mysql"],
    "mongo": ["mongodump", "mongorestore"]
}

SUPPORTED_DATABASES = ["postgres", "mysql", "mongo"]

def check_binaries(db_type: str):
    missing = []
    for binary in REQUIRED_BINARIES.get(db_type, []):
        if shutil.which(binary) is None:
            missing.append(binary)
    if len(missing) > 0:
        raise EnvironmentError(f"Missing required tools for {db_type} : {', '.join(missing)}")
    
def test_connection(config: dict):
    logger.info(f"Testing {config["db_type"]} connection...")
    if config["db_type"] == "postgres":
        # cmd = [
        #     "pg_isready",
        #     "-d", config["db_name"],
        #     "-h", config["db_host"],
        #     "-p", str(config["db_port"]),
        #     "-U", config["db_username"]
        #        ]
        cmd = ["nc", "-zv", config["db_host"], str(config["db_port"])]
    elif config["db_type"] == "mysql":
        cmd = [
            "mysqladmin",
            "-h", config["db_host"],
            "-P", str(config["db_port"]),
            "-u", config["db_username"],
            "-p", config["db_password"],
            "ping"
        ]
    elif config["db_type"] == "mongo":
        cmd = ["mongosh", "--host", config["db_host"], "--port", config["db_port"]]
        #cmd = ["mongosh", "--eval", "db.stats()", config["uri"]]
    else:
        logger.warning(f"{config["db_type"]} type not supported currently. We support {" ,".join(SUPPORTED_DATABASES)}")
        exit(1)

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"{config["db_type"].capitalize()} connection successful ✅")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to connect to {config["db_type"]}: {e.stderr.decode()}")
        raise
