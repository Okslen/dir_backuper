import csv
import time

from copy_script import copy_changed_files
from logger import get_logger

from constants import END_MSG, FILENAME, SLEEP_MSG, START_MSG, TIME_REPEAT

logger = get_logger(__name__)


def start_backup(filename: str) -> None:
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        _ = next(reader)
        for row in reader:
            copy_changed_files(row[0], row[1])


if __name__ == '__main__':
    while True:
        try:
            logger.debug(START_MSG)
            start_backup(FILENAME)
            logger.debug(SLEEP_MSG.format(TIME_REPEAT))
            time.sleep(TIME_REPEAT)
        except KeyboardInterrupt:
            logger.debug(END_MSG.format(TIME_REPEAT))
            break
        except FileNotFoundError as err:
            logger.error(f'{err.strerror} {err.filename}')
            logger.debug(SLEEP_MSG.format(TIME_REPEAT))
            time.sleep(TIME_REPEAT)
