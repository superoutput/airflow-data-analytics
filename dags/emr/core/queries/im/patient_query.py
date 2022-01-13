from hms_workflow_platform.core.queries.base.base_query import *


class PatientQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query
        self._site = site

    def patient_registration(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("SELECT format_an(an) en, format_hn(hn) hn, "
                 "(modify_date || 'T' || modify_time) mdate "
                 f"FROM visit WHERE fix_visit_type_id = '1' AND  modify_date >= '{date}'  "
                 "UNION  "
                 "SELECT format_vn(vn) en, format_hn(hn) hn, "
                 "(modify_date || 'T' || modify_time) mdate "
                 f"FROM visit WHERE fix_visit_type_id <> '1' AND  modify_date >= '{date}' ")

        result = self.query(query)
        return result if result else None

    def patient_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("select format_hn(hn) hn, (modify_date || 'T' || modify_time) mdate "
                 "from patient "
                 f"where modify_date >= '{date}'"
                 "order by mdate")

        result = self.query(query)
        return result if result else None

    def patient_update(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("select hncode hn, (modify_date || 'T' || modify_time) mdate "
                 "from patient "
                 f"where modify_date >= '{date}'")

        result = self.query(query)
        return result if result else None
