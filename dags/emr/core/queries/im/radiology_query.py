from hms_workflow_platform.core.queries.base.base_query import *


class RadiologyQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def radiology_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = (
            "select format_an(v.an) en, (xray_result.modify_date || 'T' || xray_result.modify_time) mdate from visit v"
            "left join xray_result on xray_result.visit_id = v.visit_id  AND fix_visit_type_id = '1' "
            f"where xray_result.modify_date >= '{date}'"
            "union"
            "select format_vn(v.vn) en, (xray_result.modify_date || 'T' || xray_result.modify_time) mdate from visit v"
            "left join xray_result on xray_result.visit_id = v.visit_id AND fix_visit_type_id <> '1' "
            f"where xray_result.modify_date >= '{date}'"
            "order by mdate")

        result = self.query(query)
        print(query)
        print(result)
        return result if result else None
