import datetime as dt


from file_class import Files
from logger import get_logger
from utils import get_path, make_copy, make_dir, get_scandir

from constants import FORMAT, SAVE_MSG


logger = get_logger(__name__)


def get_all_files(path: str, deep: int = 0) -> set[Files]:
    result = set()
    scandir_result = get_scandir(path)
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
    make_dir(dir_to)
    for file in (get_all_files(dir_from) - get_all_files(dir_to)):
        make_dir(get_path(dir_to + file.path, 1))
        make_copy(dir_from + file.path, dir_to + file.path)
        time = dt.datetime.fromtimestamp(file.mod_time)
        utctime = time.strftime(FORMAT)
        logger.info(SAVE_MSG.format(dir_from + file.path, utctime))
