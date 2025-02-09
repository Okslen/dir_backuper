import datetime as dt

from pathlib import Path
from typing import Set

from file_class import Files
from logger import get_logger
from utils import (get_path, make_copy, make_dir,
                   get_last_modified_by, get_scandir)

from constants import FORMAT, SAVE_MSG


logger = get_logger(__name__)


def get_all_files(path: str, deep: int = 0) -> Set[Files]:
    result = set()
    scandir_result = get_scandir(path)
    if not scandir_result:
        return result
    base_path = get_path(path, deep)
    for element in scandir_result:
        if element.name.startswith('~'):
            continue
        if element.is_file():
            file = Files(
                element.name,
                Path(element.path).relative_to(base_path),
                element.stat().st_mtime,
            )
            result.add(file)
        else:
            input_files = get_all_files(element.path, deep + 1)
            result = result.union(input_files)
    return result


def copy_changed_files(dir_from: str, dir_to: str) -> None:
    make_dir(dir_to)
    for file in get_all_files(dir_from) - get_all_files(dir_to):
        make_dir(Path(dir_to, file.path).parent)
        make_copy(Path(dir_from, file.path), Path(dir_to, file.path))
        if file.path.name.endswith(('docx', 'xlsx')):
            last_modified_by = get_last_modified_by(Path(dir_from, file.path))
            modified_by = ' ' + last_modified_by if last_modified_by else ''
        else:
            modified_by = ''
        time = dt.datetime.fromtimestamp(file.mod_time)
        utctime = time.strftime(FORMAT)
        logger.info(
            SAVE_MSG.format(
                str(Path(dir_from, file.path)),
                modified_by, utctime))
