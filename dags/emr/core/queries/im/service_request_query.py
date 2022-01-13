from hms_workflow_platform.core.queries.base.base_query import *


class ServiceRequestQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def service_request_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = (
            "SELECT format_vn(vn) as en, (mar_timetable.modify_date || 'T' || mar_timetable.modify_time) mdate FROM order_item"
            "JOIN visit ON visit.visit_id = order_item.visit_id and fix_visit_type_id  <> '1' "
            "LEFT JOIN mar_timetable ON order_item.order_item_id = mar_timetable.order_item_id AND mar_timetable.mar_date <> '' AND mar_timetable.mar_time <> ''"
            f"WHERE mar_date >= '{date}'"
            "union"
            "SELECT format_an(an) as en, (mar_timetable.modify_date || 'T' || mar_timetable.modify_time) mdate FROM order_item"
            "JOIN visit ON visit.visit_id = order_item.visit_id and fix_visit_type_id = '1'"
            "LEFT JOIN mar_timetable ON order_item.order_item_id = mar_timetable.order_item_id AND mar_timetable.mar_date <> '' AND mar_timetable.mar_time <> ''"
            f"WHERE mar_date >= '{date}'"
            "order by mdate")

        result = self.query(query)
        print(query)
        print(result)
        return result if result else None
