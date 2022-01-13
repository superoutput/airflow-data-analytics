from hms_workflow_platform.core.queries.base.base_query import *


class BillingQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def billing_create(self, date):
        return None
