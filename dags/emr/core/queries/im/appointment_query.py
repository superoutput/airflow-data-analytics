from hms_workflow_platform.core.queries.base.base_query import *


class AppointmentQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def appointment_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("SELECT  p.hncode hn, (appoi.modify_date || 'T' || appoi.modify_time) mdate "
                 "FROM appointment appoi LEFT JOIN patient p on p.patient_id = appoi.patient_id "
                 f"WHERE appoi.modify_date >= '{date}'")

        result = self.query(query)
        return result if result else None
