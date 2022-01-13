from hms_workflow_platform.core.queries.base.base_query import *


class CcQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def cc_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("SELECT format_vn(vn) en, (ddci.modify_date || 'T' || ddci.modify_time) mdate "
                 "FROM visit v "
                 f"left join doctor_discharge_ipd ddci on ddci.visit_id = v.visit_id where fix_visit_type_id <> '1' and ddci.modify_date >= '{date}' "
                 "UNION "
                 "SELECT format_an(an) en, (ddci.modify_date || 'T' || ddci.modify_time) mdate "
                 "FROM visit v "
                 f"left join doctor_discharge_ipd ddci on ddci.visit_id = v.visit_id where fix_visit_type_id = '1'  and ddci.modify_date >= '{date}' "
                 "order by mdate")

        result = self.query(query)
        return result if result else None
