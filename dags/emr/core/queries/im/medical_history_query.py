from hms_workflow_platform.core.queries.base.base_query import *


class MedicalHistoryQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def medicalhistory_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = (
            "SELECT format_vn(vn) en, (medical_history.modify_date || 'T' || medical_history.modify_time) mdate from visit "
            "LEFT JOIN patient p ON visit.patient_id = p.patient_id AND visit.active <> '0' "
            "left join medical_history on medical_history.patient_id = p.patient_id  AND fix_visit_type_id <> '1' "
            f"WHERE medical_history.modify_date >= '{date}' "
            "union "
            "SELECT format_an(an) en, (medical_history.modify_date || 'T' || medical_history.modify_time) mdate from visit "
            "LEFT JOIN patient p ON visit.patient_id = p.patient_id AND visit.active <> '0' "
            "left join medical_history on medical_history.patient_id = p.patient_id  AND fix_visit_type_id = '1' "
            f"WHERE medical_history.modify_date >= '{date}' "
            "order by mdate")

        result = self.query(query)
        return result if result else None
