
import os

from logger import get_logger


logger = get_logger(__name__)


def make_dir(dir_path: str) -> str:
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def get_path(path: str, deep: int) -> str:
    return path if deep == 0 else '\\'.join(path.split('\\')[:-deep])


def try_func(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
    except FileNotFoundError as err:
        logger.error(f'{err.strerror} {err.filename}')
    except PermissionError as err:
        logger.error(f'{err.strerror} {err.filename}')
    finally:
        return result
