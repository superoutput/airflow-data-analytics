from hms_workflow_platform.core.queries.base.base_query import *


class CarePlanQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def careplan_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("select format_an(v.an) en, (vnc.modify_date || 'T' || vnc.modify_time) mdate from visit v "
                 "inner join patient p on v.patient_id = p.patient_id "
                 "left join vs_nurse_care vnc on v.visit_id = vnc.visit_id "
                 f"where v.fix_visit_type_id = '1' and vnc.modify_date >= '{date}' "
                 "union "
                 "select format_vn(v.vn) en, (vnc.modify_date || 'T' || vnc.modify_time) mdate from visit v "
                 "inner join patient p on v.patient_id = p.patient_id "
                 "left join vs_nurse_care vnc on v.visit_id = vnc.visit_id "
                 f"where v.fix_visit_type_id <> '1' and vnc.modify_date >= '{date}' "
                 "order by mdate")

        result = self.query(query)
        return result if result else None
