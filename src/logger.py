import logging

class SingletonLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
            cls._instance._setup()
        return cls._instance

    def _setup(self):
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler = logging.FileHandler('certificate_generator.log')
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)
        self.loggers = {}

    def get_logger(self, script_name):
        if script_name not in self.loggers:
            logger = logging.getLogger(script_name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(self.file_handler)
            self.loggers[script_name] = logger
        return self.loggers[script_name]

_singleton_logger = SingletonLogger()

def get_logger(script_name):
    return _singleton_logger.get_logger(script_name)
