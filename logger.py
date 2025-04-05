import logging
from tqdm import tqdm


from constants import LOG_FORMAT, LOG_PATH, STREAM_FORMAT


class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except Exception:
            self.handleError(record)


def get_file_handler():
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return file_handler


def get_stream_handler():
    stream_handler = TqdmLoggingHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(STREAM_FORMAT))
    return stream_handler


def get_logger(name: str, log_level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    if not logger.hasHandlers():
        logger.addHandler(get_file_handler())
        logger.addHandler(get_stream_handler())
    return logger
