from hms_workflow_platform.core.queries.base.base_query import *


class AllergyQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def allergy_create(self, date_obj):
        date = date_obj.strftime('%Y-%m-%d')
        query = ("select p.hncode hn, (da.modify_date || 'T' || da.modify_time) mdate "
                 "from drug_allergy da "
                 "left join patient p on p.patient_id = da.patient_id "
                 f"where da.modify_date >= '{date}' "
                 "union "
                 "select p.hncode hn, (poa.modify_date || 'T' || poa.modify_time) mdate "
                 "from patient_other_allergy poa "
                 "left join patient p on p.patient_id = poa.patient_id "
                 f"where poa.modify_date >= '{date}'")

        result = self.query(query)
        return result if result else None
