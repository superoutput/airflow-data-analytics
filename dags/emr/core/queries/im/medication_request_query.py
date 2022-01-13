from hms_workflow_platform.core.queries.base.base_query import *


class MedicationRequestQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def medication_request_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        return None
