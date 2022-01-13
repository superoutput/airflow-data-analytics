from hms_workflow_platform.core.queries.base.base_query import *


class PiQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def pi_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("SELECT format_vn(vn) en, (vse.modify_date || 'T' || vse.modify_time) mdate "
                 "FROM visit v "
                 "left join vital_sign_extend vse on vse.visit_id = v.visit_id "
                 f"where fix_visit_type_id <> '1' and vse.modify_date >= '{date}' "
                 "UNION "
                 "SELECT format_an(an) en, (vse.modify_date || 'T' || vse.modify_time) mdate "
                 "FROM visit v "
                 "left join vital_sign_extend vse on vse.visit_id = v.visit_id "
                 f"where fix_visit_type_id = '1'  and vse.modify_date >= '{date}' "
                 "order by mdate")

        result = self.query(query)
        return result if result else None
