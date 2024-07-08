
import os
import shutil

from logger import get_logger


logger = get_logger(__name__)


def make_copy(src: str, dst: str):
    try:
        shutil.copy2(src, dst)
    except FileNotFoundError as err:
        logger.error(f'{err.strerror} {err.filename}')


def make_dir(dir_path: str) -> str:
    try:
        os.makedirs(dir_path, exist_ok=True)
    except FileNotFoundError as err:
        logger.error(f'{err.strerror} {err.filename}')


def get_path(path: str, deep: int) -> str:
    return path if deep == 0 else '\\'.join(path.split('\\')[:-deep])


def get_scandir(path: str):
    try:
        return os.scandir(path)
    except FileNotFoundError as err:
        logger.error(f'{err.strerror} {err.filename}')


def try_func(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as err:
        logger.error(f'{err.strerror} {err.filename}')
    except PermissionError as err:
        logger.error(f'{err.strerror} {err.filename}')
