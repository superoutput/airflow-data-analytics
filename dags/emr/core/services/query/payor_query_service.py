from hms_workflow_platform.core.services.base.base_service import BaseService


class PayorQueryService(BaseService):

    def __init__(self):
        super().__init__()
        self._query = None

    def prepareQuery(self, his, site):
        super().prepareQuery(his, site)

    def fetchCreated(self, **kwargs):
        list_data = self._query.payor_create(kwargs.get('yesterday'))
        return list_data

    def fetchUpdated(self, **kwargs):
        list_data = self._query.payor_update(kwargs.get('yesterday'))
        return list_data

    def generateKey(self, list_data):
        keys = self._template.payor_default(list_data)
        new_keys = self.done_list(keys)
        return new_keys
