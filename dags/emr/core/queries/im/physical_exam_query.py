from hms_workflow_platform.core.queries.base.base_query import *


class PhysicalExamQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def physicalexam_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = (
            "SELECT format_vn(vn) en, (vital_sign_extend.modify_date || 'T' || vital_sign_extend.modify_time) mdate from visit v "
            "left join vital_sign_extend on vital_sign_extend.visit_id = v.visit_id  AND fix_visit_type_id <> '1' "
            f"WHERE vital_sign_extend.examine_date >= '{date}' "
            "union "
            "SELECT format_an(an) en, (vital_sign_extend.modify_date || 'T' || vital_sign_extend.modify_time) mdate from visit v "
            "left join vital_sign_extend on vital_sign_extend.visit_id = v.visit_id  AND fix_visit_type_id = '1' "
            f"WHERE vital_sign_extend.examine_date >= '{date}' "
            "order by mdate")

        result = self.query(query)
        return result if result else None
