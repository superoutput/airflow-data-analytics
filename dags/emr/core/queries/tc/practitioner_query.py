from hms_workflow_platform.core.queries.base.base_query import *


class PractitionerQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def practitioner_create(self, date):
        query = ("SELECT CTPCP_Code employee_id, CTPCP_RowId rowid FROM CT_CareProv ORDER BY CTPCP_RowId DESC")

        result = self.query(query)
        return result if result else None
