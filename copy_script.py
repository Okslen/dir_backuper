import datetime as dt
import shutil
import os
import pytz


from file_class import Files
from logger import get_logger

from constants import FORMAT, SAVE_MSG, TIMEZONE


logger = get_logger(__name__)


def make_dir(dir_path: str) -> str:
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def get_path(path: str, deep: int) -> str:
    return path if deep == 0 else '\\'.join(path.split('\\')[:-deep])


def get_all_files(path: str, deep: int = 0) -> set[Files]:
    result = set()
    for element in os.scandir(path):
        if element.name.startswith('~'):
            continue
        if element.is_file():
            file = Files(
                element.name,
                element.path.replace(get_path(path, deep), ''),
                element.stat().st_mtime,
            )
            result.add(file)
        else:
            input_files = get_all_files(element.path, deep + 1)
            result = result.union(input_files)
    return result


def copy_file(src: str, dst: str) -> None:
    try:
        shutil.copy2(src, dst)
    except FileNotFoundError as err:
        logger.error(f'{err.strerror} {err.filename}')
    except PermissionError as err:
        logger.error(f'{err.strerror} {err.filename}')


def copy_changed_files(dir_from: str, dir_to: str) -> None:
    changed = (get_all_files(dir_from) -
               get_all_files(make_dir(dir_to)))
    for file in changed:
        make_dir(get_path(dir_to + file.path, 1))
        copy_file(dir_from + file.path, dir_to + file.path)
        time = dt.datetime.utcfromtimestamp(file.mod_time)
        utctime = time.astimezone(pytz.timezone(TIMEZONE)).strftime(FORMAT)
        logger.info(SAVE_MSG.format(dir_from + file.path, utctime))
