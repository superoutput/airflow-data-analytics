from hms_workflow_platform.core.queries.base.base_query import *


class EncounterQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def encounter_create(self, date):
        query = ("SELECT PAADM_ADMNo en, "
                 "(CAST(PAADM_UpdateDate AS VARCHAR) || 'T' || CAST(PAADM_UpdateTime AS VARCHAR)) mdate "
                 "FROM PA_Adm "
                 f"WHERE PAADM_UpdateDate >= '{date}' "
                 "AND PAADM_ADMNo IS NOT NULL "
                 "ORDER BY mdate")

        result = self.query(query)
        return result if result else None

