import logging
import logging.handlers
from datetime import datetime
from pytz import timezone
from hms_workflow_platform.settings import settings


class Logger:
    def __init__(self):
        self.timezone = datetime.now(timezone('Asia/Bangkok')).strftime('%z')

    def get_logger(self, name='root'):
        logger = logging.getLogger(name=name)
        if not logger.hasHandlers():
            self.__set_log_handler(logger)
        return logger

    def __set_log_handler(self, log_obj):
        site = settings.get('site', 'LOCAL')
        bu = settings.get('bu', '000')
        env = settings.get('env', 'DEV')
        service_name = settings.get('service_name', 'HMS-API')

        log_level = settings.get('log_level', 'INFO')
        log_format = logging.Formatter(f"%(asctime)s.%(msecs)d{self.timezone}|%(thread)d|%(process)d|{bu}-{site}-{env}|"
                                       f"%(levelname)s|%(filename)s|%(funcName)s(%(lineno)d)|{service_name}|%(message)s"
                                       , "%Y-%m-%dT%H:%M:%S")

        log_to_file = settings.get('log_to_file', False)
        if log_to_file:
            log_path = settings.get('log_path', "hms-api.log")
            rotate_when = settings.get('log_rotate_when', 'midnight')
            max_backups = settings.get('log_max_backups', 7)
            _handler = logging.handlers.TimedRotatingFileHandler(filename=log_path, when=rotate_when,
                                                                 backupCount=max_backups)
        else:
            _handler = logging.StreamHandler()
            
        _handler.setFormatter(log_format)
        log_obj.addHandler(_handler)
        log_obj.setLevel(log_level)
        log_obj.propagate = False
