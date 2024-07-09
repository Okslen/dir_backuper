import datetime as dt
import os
import pytz


for el in os.scandir(os.path.dirname(os.path.realpath(__file__))):
    print(f'{el.name} {el.stat().st_file_attributes}')


for el in os.scandir('Z:\\ПЭО\\письма_справки\\проект протокола ДК.docx'):
    print(f'{el.name} {el.stat().st_mtime}')


time = dt.datetime.fromtimestamp(456879214)
# time = dt.datetime.now()
print(time.strftime('%Y-%m-%d %H:%M:%S'))
utctime = time.strftime('%Y-%m-%d %H:%M:%S')
TIMEZONE = 'Etc/GMT-6'
tz = pytz.timezone(TIMEZONE)
print(tz)
print(utctime)
print(time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'))
