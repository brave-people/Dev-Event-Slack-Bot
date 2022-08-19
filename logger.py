
# python lib
import datetime
import logging
from logging.handlers import RotatingFileHandler

# logging set config
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s — %(message)s", 
    datefmt="%Y-%m-%d_%H:%M:%S",
    handlers=[
        RotatingFileHandler("./logs/dev-event-slack-bot.log", encoding="utf-8", maxBytes=100000000, backupCount=5)
    ]
)


# ====================================================== #

def log(message, status="info"):
    if status == "info": logging.info(message)
    else: logging.error(message)


# set process start log
def process_start_log(process_name):
    logging.info("======================================================")
    logging.info(f"{process_name} STARTED AT {datetime.datetime.now()}")
    logging.info("======================================================")
