import logging
import os
import yaml
from datetime import datetime

from pathlib import Path
from logging import StreamHandler, FileHandler, Formatter
from logging import INFO, DEBUG
from traceback import format_exc

class Log(object):
    def __init__(self) -> None:

        root_path = Path(os.path.dirname(__file__)).parent
        conf_path = os.path.join(root_path, "conf", "settings.yaml")
        try:
            with open(conf_path, "r") as yml:
                config = yaml.safe_load(yml)
            logpath = config["Logging"]["log_output"]
            loglevel = config["Logging"]["log_level"]
        except Exception:
            print(format_exc())
            print("Failed to import config.")
            return None

        # Get log level
        if loglevel == 0:
            set_level = DEBUG
        else:
            set_level = INFO

        str_format = "%(asctime)s [%(levelname)s] : %(message)s"

        # Set StreamHandler
        stream_handler = StreamHandler()
        stream_handler.setLevel(set_level)
        stream_handler.setFormatter(Formatter(str_format))

        # Set FileHandler
        file_handler = FileHandler(
            os.path.join(logpath, f"{datetime.now():%Y%m%d}.txt")
        )
        file_handler.setLevel(set_level)
        file_handler.setFormatter(
            Formatter(str_format)
        )

        # Set Root Logger
        logging.basicConfig(level=set_level, handlers=[stream_handler, file_handler])

        return None

    def debug(self, message: str) -> None:
        logging.debug(message)
        return None
        
    def warning(self, message: str) -> None:
        logging.warning(message)
        return None
        
    def info(self, message: str) -> None:
        logging.info(message)
        return None

    def error(self, message: str) -> None:
        logging.error(message)
        return None

    def critical(self, message: str) -> None:
        logging.critical(message)
        return None

log = Log()