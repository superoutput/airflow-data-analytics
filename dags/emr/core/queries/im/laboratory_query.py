from hms_workflow_platform.core.queries.base.base_query import *


class LaboratoryQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def laboratory_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        today_date, today_time = self.today_date_time()
        query = (
            "SELECT format_vn(vn) en, (lab_result.modify_date || 'T' || lab_result.modify_time) mdate from visit v "
            "left join lab_result on lab_result.visit_id = v.visit_id  AND fix_visit_type_id <> '1' "
            f"WHERE lab_result.modify_date >= '{date}' or (lab_result.modify_date = '{today_date}' and lab_result.modify_time <= '{today_time}') "
            "UNION "
            "SELECT format_an(an) en, (lab_result.modify_date || 'T' || lab_result.modify_time) mdate from visit v "
            "left join lab_result on lab_result.visit_id = v.visit_id  AND fix_visit_type_id = '1' "
            f"WHERE lab_result.modify_date >= '{date}' or (lab_result.modify_date = '{today_date}' and lab_result.modify_time <= '{today_time}') "
            "order by mdate")

        result = self.query(query)
        return result if result else None
