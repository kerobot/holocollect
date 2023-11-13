from os.path import join, dirname
from holocollect.utils.logger import get_logger

json_path = join(dirname(__file__), "configs/logger.json")
log_dir = join(dirname(__file__), "logs")
logger = get_logger(log_dir, json_path, False)
