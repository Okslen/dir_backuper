END_MSG = 'stopped by keyboard'
FILENAME = 'папки для бекапа.csv'
FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = ('%(asctime)s - [%(levelname)s] - %(name)s - '
              '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
START_MSG = 'start'
LOG_PATH = './logs/changes.log'
SAVE_MSG = '{} изменен{} в {}'
SLEEP_MSG = 'sleep {} sec'
STREAM_FORMAT = '%(asctime)s - %(message)s'
TIME_REPEAT = 600
TIME_FOR_COPY_BACKUP = 24*60*60  # время для создания незаменяемой копии в сек
