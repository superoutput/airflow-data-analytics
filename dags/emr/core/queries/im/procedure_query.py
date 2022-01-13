from hms_workflow_platform.core.queries.base.base_query import *


class ProcedureQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def procedure_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("select format_vn(vn) en, "
                 "case "
                 "when (anes_data.modify_date || 'T' || anes_data.modify_time) > (op_registered.modify_date || 'T' || op_registered.modify_time) then (anes_data.modify_date || 'T' || anes_data.modify_time) "
                 "when NULLIF(anes_data.modify_date, '') <> '' then (anes_data.modify_date || 'T' || anes_data.modify_time) "
                 "else (op_registered.modify_date || 'T' || op_registered.modify_time) end mdate "
                 "from op_registered "
                 "join visit on visit.visit_id = op_registered.visit_id "
                 "LEFT JOIN anes_data ON visit.visit_id = anes_data.visit_id "
                 f"where (op_registered.modify_date >= '{date}' or anes_data.modify_date >= '{date}') and fix_visit_type_id <> '1' "
                 "union "
                 "select format_an(an) en, "
                 "case "
                 "when (anes_data.modify_date || 'T' || anes_data.modify_time) > (op_registered.modify_date || 'T' || op_registered.modify_time) then (anes_data.modify_date || 'T' || anes_data.modify_time) "
                 "when NULLIF(anes_data.modify_date, '') <> '' then (anes_data.modify_date || 'T' || anes_data.modify_time) "
                 "else (op_registered.modify_date || 'T' || op_registered.modify_time) "
                 "end mdate "
                 "from op_registered "
                 "join visit on visit.visit_id = op_registered.visit_id "
                 "LEFT JOIN anes_data ON visit.visit_id = anes_data.visit_id "
                 f"where (op_registered.modify_date >= '{date}' or anes_data.modify_date >= '{date}') "
                 "and fix_visit_type_id = '1'order by mdate")

        result = self.query(query)
        return result if result else None
