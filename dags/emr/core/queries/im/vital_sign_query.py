from hms_workflow_platform.core.queries.base.base_query import *


class VitalSignQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def vitalsign_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        today_date, today_time = self.today_date_time()
        query = ("SELECT format_vn(vn) en,  (vt_opd.modify_date || 'T' || vt_opd.modify_time) mdate "
                 f"FROM vital_sign_opd vt_opd LEFT JOIN visit v ON vt_opd.visit_id = v.visit_id "
                 f"WHERE vt_opd.modify_date >= '{date}' or (vt_opd.modify_date = '{today_date}' "
                 f"and vt_opd.measure_time <= '{today_time}')"
                 "UNION "
                 "SELECT format_an(an) en,  (vt_ipd.modify_date || 'T' || vt_ipd.modify_time) mdate FROM "
                 f"vital_sign_ipd vt_ipd LEFT JOIN admit a ON vt_ipd.admit_id = a.admit_id "
                 f"WHERE vt_ipd.modify_date >= '{date}' or (vt_ipd.modify_date = '{today_date}' "
                 f"and vt_ipd.measure_time <= '{today_time}')"
                 "order by mdate")

        result = self.query(query)
        return result if result else None
