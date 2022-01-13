from hms_workflow_platform.core.services.base.base_service import BaseService


class AppointmentQueryService(BaseService):

    def __init__(self):
        super().__init__()
        self._query = None

    def prepareQuery(self, his, site):
        super().prepareQuery(his, site)

    def fetchCreated(self, **kwargs):
        list_data = self._query.appointment_create(kwargs.get('yesterday'))
        return list_data
