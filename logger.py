import logging


from constants import LOG_FORMAT, LOG_PATH, STREAM_FORMAT


def get_file_handler():
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(STREAM_FORMAT))
    return stream_handler


def get_logger(name: str, log_level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    if not logger.hasHandlers:
        logger.addHandler(get_file_handler())
        logger.addHandler(get_stream_handler())
    return logger
