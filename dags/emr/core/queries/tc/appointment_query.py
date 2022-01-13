from hms_workflow_platform.core.queries.base.base_query import *


class AppointmentQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def appointment_create(self, date):
        query = ("SELECT p.papmi_no hn, "
                 "(CAST(appt.APPT_TransDate AS VARCHAR) || 'T' || CAST(appt.APPT_TransTime AS VARCHAR)) mdate "
                 "FROM RB_Appointment appt LEFT JOIN pa_patmas p on p.papmi_rowid = appt.appt_papmi_dr "
                 f"WHERE appt.APPT_LastUpdateDate >= '{date}'")

        result = self.query(query)
        return result if result else None
