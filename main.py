import asyncio
import csv
import time

from pathlib import Path
from tqdm import tqdm

from copy_script import copy_changed_files_async
from logger import get_logger

from constants import (END_MSG, FILENAME, FILE_IS_EMPTY,
                       INCORRECT_ROW, SLEEP_MSG, START_MSG, TIME_REPEAT)

logger = get_logger(__name__)


async def start_backup(filename: str) -> None:
    try:
        path = Path(filename)
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            header = next(reader, None)
            if header is None:
                logger.warning(FILE_IS_EMPTY.format(filename))
            reader = list(reader)
            for index, row in tqdm(
                    enumerate(reader), total=len(reader),
                    desc='Rows processing', unit='row'):
                if len(row) < 2:
                    logger.warning(INCORRECT_ROW.format(index, filename))
                    continue
                await copy_changed_files_async(Path(row[0]), Path(row[1]))
    except FileNotFoundError as err:
        logger.error(f'{err.strerror} {err.filename}')


if __name__ == '__main__':
    while True:
        try:
            logger.info(START_MSG.format(FILENAME))
            asyncio.run(start_backup(FILENAME))
            logger.info(SLEEP_MSG.format(TIME_REPEAT))
            time.sleep(TIME_REPEAT)
        except KeyboardInterrupt:
            logger.info(END_MSG)
            break
