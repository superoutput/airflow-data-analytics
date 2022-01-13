from hms_workflow_platform.core.queries.base.base_query import *


class EncounterQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query
        self._site = site

    def encounter_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("select format_an(an) en, (modify_date || 'T' || modify_time) mdate "
                 "from visit "
                 f"where fix_visit_type_id = '1' and modify_date >= '{date}' "
                 "union "
                 "select format_vn(vn) en, (modify_date || 'T' || modify_time) mdate "
                 "from visit "
                 f"where fix_visit_type_id <> '1' and modify_date >= '{date}' "
                 "order by mdate")

        result = self.query(query)
        return result if result else None

    def encounter_discharge(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = (
            "select format_vn(vn) en, (visit.financial_discharge_date || 'T' || visit.financial_discharge_time) mdate "
            "from visit "
            f"where visit.financial_discharge_date >= '{date}' and visit.fix_visit_type_id != '1' "
            "union "
            "select format_an(an) en, (visit.financial_discharge_date || 'T' || visit.financial_discharge_time) mdate "
            "from visit "
            f"where visit.financial_discharge_date >= '{date}' and visit.fix_visit_type_id = '1' "
            "union "
            "select format_vn(vn) en, (visit.doctor_discharge_date || 'T' || visit.doctor_discharge_time) mdate "
            "from visit "
            f"where visit.doctor_discharge_date >= '{date}' and visit.fix_visit_type_id != '1' "
            "union "
            "select format_an(an) en, (visit.doctor_discharge_date || 'T' || visit.doctor_discharge_time) mdate "
            "from visit "
            f"where visit.doctor_discharge_date >= '{date}' and visit.fix_visit_type_id = '1' "
            "union "
            "select format_an(an) en, (admit.ipd_discharge_date || 'T' || admit.ipd_discharge_time) mdate "
            "from admit "
            f"where admit.ipd_discharge_date >= '{date}'")

        result = self.query(query)
        return result if result else None
