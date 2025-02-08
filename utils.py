import functools
import os
import shutil
import xml.dom.minidom
import zipfile


from logger import get_logger
from zipfile import BadZipFile

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
        except OSError as err:
            logger.error(f'{err.strerror} {err.filename}')
        except BadZipFile:
            logger.error('')
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


@try_func
def get_last_modified_by(path: str) -> str:
    document = zipfile.ZipFile(path)
    # Open/read the core.xml (contains the last user).
    try:
        uglyXML = xml.dom.minidom.parseString(
            document.read('docProps/core.xml')).toprettyxml(indent='  ')
    except KeyError as err:
        logger.error(f'{err} {path}')
        return ''
    asText = uglyXML.splitlines()
    for item in asText:
        if 'lastModifiedBy' in item:
            itemLength = len(item)-20
            return item[21:itemLength]
