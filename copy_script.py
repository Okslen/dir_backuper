import datetime as dt
import shutil
import os
import pytz


from file_class import Files
from logger import get_logger
from utils import get_path, make_dir, try_func

from constants import FORMAT, SAVE_MSG, TIMEZONE


logger = get_logger(__name__)


def get_all_files(path: str, deep: int = 0) -> set[Files]:
    result = set()
    scandir_result = try_func(os.scandir, path)
    if scandir_result:
        for element in scandir_result:
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


def copy_changed_files(dir_from: str, dir_to: str) -> None:
    changed = (get_all_files(dir_from) -
               get_all_files(try_func(make_dir, dir_to)))
    for file in changed:
        try_func(make_dir, get_path(dir_to + file.path, 1))
        try_func(shutil.copy2, dir_from + file.path, dir_to + file.path)
        time = dt.datetime.fromtimestamp(file.mod_time)
        utctime = time.astimezone(pytz.timezone(TIMEZONE)).strftime(FORMAT)
        logger.info(SAVE_MSG.format(dir_from + file.path, utctime))
