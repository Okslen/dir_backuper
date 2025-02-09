import csv
import time

from pathlib import Path

from copy_script import copy_changed_files
from logger import get_logger

from constants import (END_MSG, FILENAME, FILE_IS_EMPTY,
                       INCORRECT_ROW, SLEEP_MSG, START_MSG, TIME_REPEAT)

logger = get_logger(__name__)


def start_backup(filename: str) -> None:
    try:
        path = Path(filename)
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            header = next(reader, None)
            if header is None:
                logger.warning(FILE_IS_EMPTY.format(filename))
            for index, row in enumerate(reader):
                if len(row) < 2:
                    logger.warning(INCORRECT_ROW.format(index, filename))
                copy_changed_files(Path(row[0]), Path(row[1]))
    except FileNotFoundError as err:
        logger.error(f'{err.strerror} {err.filename}')


if __name__ == '__main__':
    while True:
        try:
            logger.debug(START_MSG.format(FILENAME))
            start_backup(FILENAME)
            logger.debug(SLEEP_MSG.format(TIME_REPEAT))
            time.sleep(TIME_REPEAT)
        except KeyboardInterrupt:
            logger.debug(END_MSG)
            break
