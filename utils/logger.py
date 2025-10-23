import logging

#TODO: read more into logging and migrate to loguru
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("backup.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)