from hms_workflow_platform.core.common.utils.database.adapter import Adapter
from hms_mongo_driver import HMSMongoDriver
from hms_workflow_platform.core.common.utils.logger.logger import Logger
from hms_workflow_platform.settings import settings
from pytz import timezone
from datetime import datetime, timedelta


class BaseQuery:
    def __init__(self):
        self.logger = Logger().get_logger()

    @staticmethod
    def get_mongodb_commander():
        setting_mongo = settings.get('his_mongodb')
        return HMSMongoDriver(setting_mongo)

    @staticmethod
    def get_adapter(key):
        return Adapter(his_adapter=key)

    def ten_days_ago(self):
        today = datetime.now(timezone('Asia/Bangkok'))
        days_ago = today - timedelta(days=10)
        return days_ago.strftime('%Y-%m-%d')

    def today_date_time(self):
        today = datetime.now(timezone('Asia/Bangkok'))
        today_date = today.strftime('%Y-%m-%d')
        today_time = today.strftime('%H-%M-%S')
        return today_date, today_time