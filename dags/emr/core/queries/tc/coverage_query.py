from hms_workflow_platform.core.queries.base.base_query import *


class CoverageQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def coverage_create(self, date):
        query = (
            "SELECT "
            "PA_Adm.PAADM_ADMNo en, "
            "(CAST(PA_AdmInsurance.INS_UpdateDate AS VARCHAR) || 'T' || CAST(PA_AdmInsurance.INS_UpdateTime AS VARCHAR)) mdate "
            "FROM "
            "PA_Adm "
            "INNER JOIN PA_AdmInsurance ON "
            "PA_Adm.PAADM_ROWID = PA_AdmInsurance.INS_ParRef "
            "WHERE "
            "PA_Adm.PAADM_ADMNo IS NOT NULL "
            f"AND PA_Adm.PAADM_UpdateDate >= '{date}'")

        result = self.query(query)
        return result if result else None
