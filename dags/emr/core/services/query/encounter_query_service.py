from hms_workflow_platform.core.common.utils.rabbitMQ_manager import RabbitMQ
from hms_workflow_platform.core.services.base.base_service import BaseService
from hms_workflow_platform.settings import settings


class EncounterQueryService(BaseService):
    def __init__(self):
        super().__init__()
        self._query = None

    def prepareQuery(self, his, site):
        super().prepareQuery(his, site)

    def fetchCreated(self, **kwargs):
        list_data = self._query.encounter_create(kwargs.get('yesterday'))
        return list_data

    def fetchUpdated(self, **kwargs):
        list_data = self._query.encounter_update(kwargs.get('yesterday'))
        return list_data

    def fetchDischarge(self, **kwargs):
        list_data = self._query.encounter_discharge(kwargs.get('yesterday'))
        return list_data
