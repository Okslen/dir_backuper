import asyncio
import datetime as dt
import os
import shutil
import xml.dom.minidom
import zipfile


from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


from constants import BAD_ZIP_FILE, FORMAT, SAVE_MSG
from file_class import Files
from logger import get_logger
from zipfile import BadZipFile

logger = get_logger(__name__)


def get_last_modified_by(path: Path) -> str:
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


def make_copy(file: Files, src: Path, dst: Path):
    try:
        shutil.copy2(src, dst)
        if file.path.suffix in {'.docx', '.xlsx'}:
            last_modified_by = get_last_modified_by(src)
            modified_by = ' ' + last_modified_by if last_modified_by else ''
        else:
            modified_by = ''
        utctime = dt.datetime.fromtimestamp(file.mod_time).strftime(FORMAT)
        logger.info(
            SAVE_MSG.format(src, modified_by, utctime))
    except (FileNotFoundError, PermissionError, OSError) as err:
        logger.error(f'{err.strerror} {err.filename}')
    return None


async def make_copy_async(
        file: Files, src: Path, dst: Path, executor: ThreadPoolExecutor):
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(executor, make_copy, file, src, dst)
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


def get_scandir(path: str):
    try:
        return os.scandir(path)
    except (PermissionError, OSError) as err:
        logger.error(f'{err.strerror} {err.filename}')
    return []
