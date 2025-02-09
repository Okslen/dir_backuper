import asyncio

from pathlib import Path
from tqdm import tqdm
from typing import Set

from file_class import Files
from logger import get_logger
from utils import (get_path, make_copy_async, make_dir, get_scandir)

from constants import (CHANGED_FILES_MSG, GET_ALL_FILES_MSG, START_MSG)


logger = get_logger(__name__)


def get_all_files(path: Path, deep: int = 0) -> Set[Files]:
    result = set()
    scandir_result = get_scandir(path)
    if scandir_result is None:
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


async def copy_changed_files_async(dir_from: Path, dir_to: Path):
    make_dir(dir_to)
    logger.info(START_MSG.format(dir_from))
    src_files = get_all_files(dir_from)
    logger.info(GET_ALL_FILES_MSG.format(dir_from, len(src_files)))
    logger.info(START_MSG.format(dir_to))
    dst_files = get_all_files(dir_to)
    logger.info(GET_ALL_FILES_MSG.format(dir_to, len(dst_files)))
    changed_files = src_files - dst_files
    logger.info(CHANGED_FILES_MSG.format(len(changed_files), dir_from, dir_to))
    tasks = []
    for file in tqdm(
            changed_files, desc='Files processing',
            unit='file', colour="green", ncols=80):
        src_path, dst_path = Path(dir_from, file.path), Path(dir_to, file.path)
        make_dir(dst_path.parent)
        tasks.append(make_copy_async(file, src_path, dst_path))

    await asyncio.gather(*tasks)
