DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3


class Logger:
    def __init__(self, level=INFO):
        self.level = level

    def log(self, message, level):
        if level >= self.level:
            print(f'[{level}] {message}')

    def debug(self, message):
        self.log(message, DEBUG)

    def info(self, message):
        self.log(message, INFO)

    def warn(self, message):
        self.log(message, WARN)

    def error(self, message):
        self.log(message, ERROR)
