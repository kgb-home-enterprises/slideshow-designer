import datetime

DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3

logger_count = 0


class Logger:
    def __init__(self, name=None, level=INFO):
        global logger_count
        self.name = name or f'DefaultLogger__{logger_count}'
        self.level = level
        self.level_names = {
            DEBUG: 'DEBUG',
            INFO: 'INFO',
            WARN: 'WARN',
            ERROR: 'ERROR'
        }
        logger_count += 1

    def set_level(self, level):
        self.level = level

    def set_level_name(self, level, name):
        self.level_names[level] = name

    def log(self, message, level):
        if level >= self.level:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'[{timestamp}] [{self.name}] [{self.level_names.get(level, level)}] {message}')

    def debug(self, message):
        self.log(message, DEBUG)

    def info(self, message):
        self.log(message, INFO)

    def warn(self, message):
        self.log(message, WARN)

    def error(self, message):
        self.log(message, ERROR)
