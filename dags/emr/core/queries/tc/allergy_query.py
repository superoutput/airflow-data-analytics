from hms_workflow_platform.core.queries.base.base_query import *



class AllergyQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def allergy_create(self, date):
        ten_days_ago_date = self.ten_days_ago()
        query = ("SELECT (SELECT PAPMI_NO FROM PA_Patmas WHERE papmi_rowid = pa.paadm_papmi_dr) hn, "
                 "(CAST(paa.ALG_LastUpdateDate AS VARCHAR) || 'T' || CAST(paa.ALG_LastUpdateTime AS VARCHAR)) mdate "
                 "FROM PA_Adm pa "
                 "INNER JOIN PA_Allergy paa on pa.paadm_papmi_dr = paa.ALG_PAPMI_ParRef "
                 f"WHERE pa.PAADM_UpdateDate >= '{ten_days_ago_date}' and paa.ALG_LastUpdateDate >= '{date}'")

        result = self.query(query)
        return result if result else None
