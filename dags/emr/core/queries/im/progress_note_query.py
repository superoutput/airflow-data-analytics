from hms_workflow_platform.core.queries.base.base_query import *


class ProgressNoteQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def progress_note_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("SELECT case when v.fix_visit_type_id <> '1' then format_vn(v.vn) else format_an(v.an) end en, "
                 "(pn.modify_date || 'T' || pn.modify_time) mdate "
                 "from visit v inner join progress_note pn on v.visit_id = pn.visit_id "
                 f"where pn.modify_date >= '{date}' ")
        result = self.query(query)
        return result if result else None
