"""
The logger module for the TSM Accounting Manager application.
"""
import logging
from .config import log_file, logging_level

# configure the file handler
file_handler = logging.FileHandler(log_file, mode="w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s"))

# configure the stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s"))

# create the logger object
logger = logging.getLogger("tsmaccountingmanager")
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging_level)
