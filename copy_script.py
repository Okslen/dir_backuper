import asyncio

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from file_class import Files
from logger import get_logger
from utils import make_copy_async, make_dir, get_scandir

from constants import (CHANGED_FILES_MSG, GET_ALL_FILES_MSG, START_MSG)


logger = get_logger(__name__)


async def get_all_files_async(
        path: Path, executor: ThreadPoolExecutor,
        base_path: Path = None) -> set[Files]:
    result = set()
    loop = asyncio.get_running_loop()
    scandir_result = await loop.run_in_executor(executor, get_scandir, path)
    tasks = []
    if base_path is None:
        base_path = path
    for element in scandir_result:
        if element.name.startswith('~') or element.name in {'Thumbs.db'}:
            continue
        element_path = Path(element.path)
        if element.is_file():
            result.add(Files(
                element_path.relative_to(base_path),
                element.stat().st_mtime,
            ))
        else:
            tasks.append(asyncio.create_task(
                get_all_files_async(element_path, executor, base_path)))

    if tasks:
        for scanned_files in await asyncio.gather(*tasks):
            result.update(scanned_files)
    return result


async def copy_changed_files_async(
        dir_from: Path, dir_to: Path, executor: ThreadPoolExecutor):
    make_dir(dir_to)
    logger.debug(START_MSG.format(dir_from))
    logger.debug(START_MSG.format(dir_to))
    src_files_task = asyncio.create_task(
        get_all_files_async(dir_from, executor))
    dst_files_task = asyncio.create_task(
        get_all_files_async(dir_to, executor))
    src_files, dst_files = await asyncio.gather(src_files_task, dst_files_task)
    logger.debug(GET_ALL_FILES_MSG.format(dir_from, len(src_files)))
    logger.debug(GET_ALL_FILES_MSG.format(dir_to, len(dst_files)))
    changed_files = src_files - dst_files
    tasks = []
    if changed_files:
        logger.info(
            CHANGED_FILES_MSG.format(len(changed_files), dir_from, dir_to))
        for file in changed_files:
            src_path, dst_path = Path(
                dir_from, file.path), Path(dir_to, file.path)
            make_dir(dst_path.parent)
            tasks.append(make_copy_async(file, src_path, dst_path, executor))

    await asyncio.gather(*tasks)
