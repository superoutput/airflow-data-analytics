from hms_workflow_platform.core.queries.base.base_query import *


class DiagnosisQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def diagnostic_create(self, date):
        ten_days_ago_date = self.ten_days_ago()
        query = (
            "SELECT pa.PAADM_ADMNo en, "
            "(CAST(mrd.MRDIA_UpdateDate AS VARCHAR) || 'T' || CAST(mrd.MRDIA_UpdateTime AS VARCHAR)) mdate "
            "FROM MR_Diagnos mrd "
            f"INNER JOIN PA_Adm pa ON pa.PAADM_UpdateDate >= '{ten_days_ago_date}' AND "
            f"pa.PAADM_UpdateDate <= '{date}' AND pa.PAADM_MainMRADM_DR = mrd.MRDIA_MRADM_ParRef "
            f"WHERE mrd.MRDIA_UpdateDate = '{date}' OR mrd.MRDIA_Date = '{date}' "
            "ORDER BY mdate")

        result = self.query(query)
        return result if result else None
