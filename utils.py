import functools
import os
import shutil

from logger import get_logger


logger = get_logger(__name__)


def try_func(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as err:
            logger.error(f'{err.strerror} {err.filename}')
        except PermissionError as err:
            logger.error(f'{err.strerror} {err.filename}')
    return wrapper


@try_func
def make_copy(src: str, dst: str):
    shutil.copy2(src, dst)


@try_func
def make_dir(dir_path: str) -> str:
    os.makedirs(dir_path, exist_ok=True)


def get_path(path: str, deep: int) -> str:
    return path if deep == 0 else '\\'.join(path.split('\\')[:-deep])


@try_func
def get_scandir(path: str):
    return os.scandir(path)
