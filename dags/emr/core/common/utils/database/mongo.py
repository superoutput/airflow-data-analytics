import traceback
from pymongo import MongoClient, errors
from hms_workflow_platform.core.common.utils.singleton import SingletonMetaClass
from hms_workflow_platform.core.common.utils.logger.logger import Logger
from hms_workflow_platform.core.common.utils.logger.standard_message import StandardMessage
from hms_workflow_platform.core.common.utils.custom_exceptions import MongoDBManagerError
from hms_workflow_platform.settings import settings


class MongoDBManager(metaclass=SingletonMetaClass):
    def __init__(self, mongo_settings):
        self._logger = Logger().get_logger()
        self.get_settings = mongo_settings
        self._client, self.db = self._create_client()

    def _create_client(self):
        mongodb_setting = settings.get(self.get_settings, None)
        if mongodb_setting is None:
            msg = StandardMessage.ERROR_MONGODB_MISSING_SETTING.format(key='mongodb')
            self._logger.error(msg)
            raise MongoDBManagerError(msg)

        host = mongodb_setting.get('host', None)
        port = mongodb_setting.get('port', None)
        database = mongodb_setting.get('database', None)
        if host is None or port is None or database is None:
            key = list()
            if host is None:
                key.append('host')
            if port is None:
                key.append('port')
            if database is None:
                key.append('database')
            msg = StandardMessage.ERROR_MONGODB_MISSING_SETTING.format(key=', '.join(key))
            self._logger.error(msg)
            raise MongoDBManagerError(msg)

        kwargs = dict()
        if isinstance(host, list):
            replica_set = mongodb_setting.get('replica_set', None)
            if replica_set is not None:
                kwargs.update({
                    'replicaSet': replica_set,
                    'readPreference': 'secondaryPreferred'
                })
            else:
                msg = StandardMessage.ERROR_MONGODB_MISSING_SETTING.format(key='replica_set')
                self._logger.error(msg)
                raise MongoDBManagerError(msg)

        user = mongodb_setting.get('user', None)
        password = mongodb_setting.get('password', None)
        mechanism = mongodb_setting.get('mechanism', None)
        if user is not None and password is not None and mechanism is not None:
            kwargs.update({
                'username': user,
                'password': password,
                'authSource': database,
                'authMechanism': mechanism
            })
        client = MongoClient(host=host, port=port, connect=False, **kwargs)
        try:
            info = client.server_info
            if info:
                self._logger.info(StandardMessage.INFO_MONGODB_CONNECTED)
        except errors.ServerSelectionTimeoutError:
            error_msg = StandardMessage.ERROR_MONGODB_CONNECTION_REFUSE
            self._logger.error(error_msg)
            raise MongoDBManagerError(error_msg)
        except Exception:
            error_msg = StandardMessage.ERROR_UNHANDLED_EXCEPTION.format(error=traceback.format_exc())
            self._logger.error(error_msg)
            raise MongoDBManagerError(error_msg)
        return client, client[database]

    def _check_collection(self, collection):
        if isinstance(collection, str):
            return True
        else:
            self._logger.error(StandardMessage.ERROR_MONGODB_COLLECTION_TYPE.format(type=type(collection)))
            return False

    def _check_data(self, data):
        if isinstance(data, dict):
            return True
        elif isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    self._logger.error(StandardMessage.ERROR_MONGODB_DATA_LIST_TYPE.format(type=type(item)))
                    return False
        else:
            self._logger.error(StandardMessage.ERROR_MONGODB_DATA_TYPE.format(type=type(data)))
            return False

    def _check_query(self, query):
        if isinstance(query, dict):
            return True
        else:
            self._logger.error(StandardMessage.ERROR_MONGODB_QUERY_TYPE.format(type=type(query)))
            return False

    def _check_pipeline(self, pipeline):
        if isinstance(pipeline, list):
            return True
        else:
            self._logger.error(StandardMessage.ERROR_MONGODB_QUERY_TYPE.format(type=type(query)))
            return False

    def close_client(self):
        self._client.close()

    def insert(self, collection, data):
        try:
            if self._check_collection(collection) and self._check_data(data):
                if isinstance(data, dict):
                    return self.db[collection].insert_one(document=data).inserted_id
                elif isinstance(data, list):
                    return self.db[collection].insert_many(document=data).inserted_ids
            else:
                return None
        except Exception:
            msg = StandardMessage.ERROR_UNHANDLED_EXCEPTION.format(error=traceback.format_exc())
            self._logger.error(msg)
            raise MongoDBManagerError(msg)

    def update(self, collection, query, data, one=True):
        try:
            if self._check_collection(collection) and self._check_data(data) and self._check_query(query):
                if one:
                    return self.db[collection].update_one(filter=query, update=data).modified_count
                else:
                    return self.db[collection].update_many(filter=query, update=data).modified_count
            else:
                return None
        except Exception:
            msg = StandardMessage.ERROR_UNHANDLED_EXCEPTION.format(error=traceback.format_exc())
            self._logger.error(msg)
            raise MongoDBManagerError(msg)

    def replace(self, collection, query, data):
        try:
            if self._check_collection(collection) and self._check_data(data) and self._check_query(query):
                return self.db[collection].replace_one(filter=query, replacement=data, upsert=True).modified_count
            else:
                return None
        except Exception:
            msg = StandardMessage.ERROR_UNHANDLED_EXCEPTION.format(error=traceback.format_exc())
            self._logger.error(msg)
            raise MongoDBManagerError(msg)

    def find(self, collection, query, one=False, limit=0):
        try:
            if self._check_collection(collection) and self._check_query(query):
                if '_id' in query:
                    return self.db[collection].find_one(filter={'_id': query['_id']})

                if one:
                    return self.db[collection].find_one(filter=query)
                else:
                    return self.db[collection].find(filter=query, limit=limit)
            else:
                return None
        except Exception:
            msg = StandardMessage.ERROR_UNHANDLED_EXCEPTION.format(error=traceback.format_exc())
            self._logger.error(msg)
            raise MongoDBManagerError(msg)

    def aggregate(self, collection, pipeline=[], **kwargs):
        try:
            if self._check_collection(collection) and self._check_pipeline(pipeline):
                return self.db[collection].aggregate(pipeline, **kwargs)
            else:
                return None
        except Exception:
            msg = StandardMessage.ERROR_UNHANDLED_EXCEPTION.format(error=traceback.format_exc())
            self._logger.error(msg)
            raise MongoDBManagerError(msg)