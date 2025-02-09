import os
import shutil
import xml.dom.minidom
import zipfile


from pathlib import Path


from constants import BAD_ZIP_FILE, DIR_NOT_EXIST
from logger import get_logger
from zipfile import BadZipFile

logger = get_logger(__name__)


def make_copy(src: Path, dst: Path):
    try:
        shutil.copy2(src, dst)
    except (FileNotFoundError, PermissionError, OSError) as err:
        logger.error(f'{err.strerror} {err.filename}')
    return None


def make_dir(dir_path: Path):
    try:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as err:
        logger.error(f'{err.strerror} {err.filename}')
    return None


def get_path(path: str, deep: int) -> Path:
    result = Path(path).parents[deep - 1] if deep > 0 else Path(path)
    return result


def get_scandir(path: str):
    try:
        if not os.path.exists(path):
            logger.error(DIR_NOT_EXIST.format(path))
        return os.scandir(path)
    except (PermissionError, OSError) as err:
        logger.error(f'{err.strerror} {err.filename}')
    return None


def get_last_modified_by(path: str) -> str:
    try:
        with zipfile.ZipFile(path) as document:
            uglyXML = xml.dom.minidom.parseString(
                document.read('docProps/core.xml')).toprettyxml(indent='  ')
    except KeyError as err:
        logger.error(f'{err} {path}')
        return ''
    except BadZipFile:
        logger.error(BAD_ZIP_FILE)
    asText = uglyXML.splitlines()
    for item in asText:
        if 'lastModifiedBy' in item:
            itemLength = len(item)-20
            return item[21:itemLength]
    return ''
