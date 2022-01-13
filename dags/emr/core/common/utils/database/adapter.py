import json
import requests
import traceback
from hms_workflow_platform.settings import settings
from time import time
from hms_workflow_platform.core.common.utils.custom_exceptions import AdapterError, AdapterQueryError
from hms_workflow_platform.core.common.utils.http.url import slash_join
from hms_workflow_platform.core.common.utils.logger.logger import Logger
from hms_workflow_platform.core.common.utils.logger.standard_message import StandardMessage


class Adapter:
    def __init__(self, his_adapter):
        self._logger = Logger().get_logger()
        self._url = settings.get('adapter_url', dict())
        if not self._url:
            msg = StandardMessage.ERROR_ADAPTER_URL_NOT_FOUND.format(key=his_adapter)
            self._logger.error(msg)
            raise AdapterError(msg)

    def _request(self, url, headers, body, method='POST'):
        start = time()
        try:
            self._logger.debug(StandardMessage.DEBUG_REQUEST_URL.format(method=method, url=url, headers=headers,
                                                                        body=json.dumps(body)))
            res = requests.request(method=method, url=url, data=body, headers=headers, timeout=10000)
            end = time()
            status_code = res.status_code
            try:
                result = res.json()
                result_str = json.dumps(result)
            except:
                result_str = result = res.text

            if 200 <= res.status_code < 300:
                self._logger.info(StandardMessage.INFO_RESPONSE_URL.format(method=method, url=url, status=status_code))
                self._logger.debug(StandardMessage.DEBUG_RESPONSE_URL.format(method=method, url=url, status=status_code,
                                                                             response=result_str))
                return result.get('data')
            elif 417 == res.status_code:
                return "SQLException"
            else:
                msg = StandardMessage.WARNING_RESPONSE_URL.format(method=method, url=url, status=status_code,
                                                                  response=result_str)
                self._logger.warning(msg)
                raise AdapterQueryError(msg)
        except AdapterQueryError as e:
            raise e
        except Exception:
            tb = traceback.format_exc()
            end = time()
            msg = StandardMessage.ERROR_REQUEST_URL.format(method=method, url=url, error=tb)
            self._logger.error(msg)
            raise AdapterError(msg)

    def query(self, sql, serialized=True, timeout=5):
        url = slash_join(self._url, '/query')
        headers = {"content-type": "application/x-www-form-urlencoded"}
        body = {"sql": sql, "timeout": timeout, "serialized": serialized}
        result = self._request(url=url, headers=headers, body=body)
        return result or list()

    def aggregate(self, collection, aggregate, serialized=False, timeout=5):
        url = slash_join(self._url, '/query')
        headers = {"content-type": "application/x-www-form-urlencoded"}
        body = {"collection": collection, "aggregate": json.dumps(aggregate), "serialized": serialized,
                "timeout": timeout}
        result = self._request(url=url, headers=headers, body=body)
        return result or list()

    def update(self, sql, is_returning=False):
        url = slash_join(self._url, '/update')
        headers = {"content-type": "application/x-www-form-urlencoded"}
        body = {"sql": sql, "returning": True} if is_returning else {"sql": sql}
        result = self._request(url=url, headers=headers, body=body)
        return result or list()

    def execute(self, sql):
        url = slash_join(self._url, '/execute')
        headers = {"content-type": "application/x-www-form-urlencoded"}
        body = {"sql": sql, "key": "yaw3tag-sMh-t3rc3s"}
        result = self._request(url=url, headers=headers, body=body)
        return result or list()
