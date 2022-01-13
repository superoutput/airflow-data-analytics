from hms_workflow_platform.core.queries.base.base_query import *


class CoverageQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def coverage_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("SELECT format_vn(vn) en, (visit.modify_date || 'T' || visit.modify_time) mdate from visit "
                 "inner join visit_payment on visit_payment.visit_id = visit.visit_id AND visit.fix_visit_type_id <> '1' "
                 f"where  visit.active  <> '0' and visit.modify_date >= '{date}' "
                 "union "
                 "SELECT format_an(an) en, (visit.modify_date || 'T' || visit.modify_time) mdate from visit "
                 "inner join visit_payment on visit_payment.visit_id = visit.visit_id AND visit.fix_visit_type_id = '1' "
                 f"where  visit.active  <> '0' and visit.modify_date >= '{date}' "
                 "order by mdate")

        result = self.query(query)
        return result if result else None
