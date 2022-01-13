import abc
from hms_workflow_platform.core.services.builder import Builder
from hms_workflow_platform.core.common.utils.redis_manager import *
from datetime import datetime
from pytz import timezone
from hms_workflow_platform.core.common.utils.logger.logger import Logger


class BaseService(metaclass=abc.ABCMeta):
    def __init__(self):
        self._redis_m = Redis_manager()
        self.logger = Logger().get_logger()
        self._query = None
        self._template = None

    def prepareQuery(self, his, site):
        _builder = Builder(self)
        self._query = _builder.getQuery(his, site)

    def prepareTemplate(self, his):
        _builder = Builder(self)
        self._template = _builder.getTemplate(his)

    def done_list(self, data_list):
        data_not_exists = []
        for key in data_list:
            if self._redis_m.r_exists(key + "ZZZ") == 0:
                data_not_exists.append(key + "ZZZ")
                date_now = datetime.now(timezone('Asia/Bangkok'))
                date_str = date_now.strftime('%Y-%m-%d %H:%M:%S')
                self._redis_m.r_setex(key + "ZZZ", 60, date_str)
        return data_not_exists
