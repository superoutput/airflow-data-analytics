from hms_workflow_platform.core.queries.base.base_query import *


class ProcedureQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def procedure_create(self, date):
        query = ("SELECT PAADM_ADMNo en, "
                 "(CAST(orao.ANAOP_UpdateDate AS VARCHAR) || 'T' || CAST(orao.ANAOP_UpdateTime AS VARCHAR)) mdate "
                 "FROM OR_Anaesthesia ora "
                 "INNER JOIN OR_Anaest_Operation orao ON ora.ANA_RowId = orao.ANAOP_Par_Ref "
                 "INNER JOIN ORC_Operation orc ON orc.OPER_RowId = orao.ANAOP_Type_DR "
                 "INNER JOIN PA_Adm pa ON pa.PAADM_rowid = ora.ANA_PAADM_ParRef "
                 f"WHERE orao.ANAOP_UpdateDate >= '{date}' AND PAADM_ADMNo IS NOT NULL "
                 "ORDER BY mdate")

        result = self.query(query)
        return result if result else None

