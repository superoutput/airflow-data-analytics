from hms_workflow_platform.core.queries.base.base_query import *


class ClaimQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def claim_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        return None
