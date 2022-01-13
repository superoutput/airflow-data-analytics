from hms_workflow_platform.core.services.base.base_service import BaseService


class PractitionerQueryService(BaseService):

    def __init__(self):
        super().__init__()
        self._query = None

    def prepareQuery(self, his, site):
        super().prepareQuery(his, site)

    def fetchCreated(self, **kwargs):
        list_data = self._query.practitioner_create(kwargs.get('yesterday'))
        return list_data

    def fetchUpdated(self, **kwargs):
        list_data = self._query.practitioner_update(kwargs.get('yesterday'))
        return list_data
