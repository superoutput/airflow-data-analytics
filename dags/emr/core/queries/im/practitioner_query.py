from hms_workflow_platform.core.queries.base.base_query import *


class PractitionerQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def practitioner_create(self, date):
        query = ("SELECT employee_id, rowid FROM employee ORDER BY rowid DESC ")

        result = self.query(query)
        return result if result else None
