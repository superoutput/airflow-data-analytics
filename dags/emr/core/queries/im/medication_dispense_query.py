from hms_workflow_platform.core.queries.base.base_query import *


class MedicationDispenseQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def medication_dispense_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("select format_an(v.an) en, (ori.dispense_date || 'T' || ori.dispense_time) mdate FROM visit v "
                 "LEFT JOIN order_item ori ON v.visit_id = ori.visit_id and ori.fix_item_type_id = '0' "
                 f"where v.fix_visit_type_id = '1' and ori.dispense_date >= '{date}' "
                 "union "
                 "select format_vn(v.vn) en, (ori.dispense_date || 'T' || ori.dispense_time) mdate FROM visit v "
                 "LEFT JOIN order_item ori ON v.visit_id = ori.visit_id and ori.fix_item_type_id = '0' "
                 f"where v.fix_visit_type_id <> '1' and ori.dispense_date >= '{date}'")

        result = self.query(query)
        return result if result else None
