from hms_workflow_platform.core.queries.base.base_query import *


class DiagnosisQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def diagnostic_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        today_date, today_time = self.today_date_time()
        query = (
            "SELECT format_vn(vn) en, (diagnosis_icd10.modify_date || 'T' || diagnosis_icd10.modify_time) mdate "
            f"FROM diagnosis_icd10 JOIN visit ON visit.visit_id = diagnosis_icd10.visit_id AND fix_visit_type_id <> '1' "
            f"WHERE diagnosis_icd10.modify_date >= '{date}' or (diagnosis_icd10.modify_date = '{today_date}' "
            f"and diagnosis_icd10.modify_time <= '{today_time}')"
            "UNION "
            "SELECT format_an(an) en, (diagnosis_icd10.modify_date || 'T' || diagnosis_icd10.modify_time) mdate FROM "
            f"diagnosis_icd10 JOIN visit ON visit.visit_id = diagnosis_icd10.visit_id AND fix_visit_type_id = '1' "
            f"WHERE diagnosis_icd10.modify_date >= '{date}' or (diagnosis_icd10.modify_date = '{today_date}' "
            f"and diagnosis_icd10.modify_time <= '{today_time}')"
            "order by mdate")

        result = self.query(query)
        return result if result else None

