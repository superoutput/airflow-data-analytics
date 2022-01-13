from hms_workflow_platform.core.services.base.base_service import BaseService

class PatientQueryService(BaseService):

    def __init__(self):
        super().__init__()
        self._query = None

    def prepareQuery(self, his, site):
        super().prepareQuery(his, site)

    def fetchCreated(self, **kwargs):
        list_data = self._query.patient_create(kwargs.get('yesterday'))
        print(list_data)
        # return list_data

    def fetchRegistration(self, **kwargs):
        list_data = self._query.patient_registration(kwargs.get('yesterday'))
        return list_data

    def fetchUpdated(self, **kwargs):
        list_data = self._query.patient_update(kwargs.get('yesterday'))
        return list_data
