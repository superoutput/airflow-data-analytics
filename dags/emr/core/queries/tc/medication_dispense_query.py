from hms_workflow_platform.core.queries.base.base_query import *


class MedicationDispenseQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def medication_dispense_create(self, date):
        query = (
            "SELECT pa.PAADM_ADMNo en, "
            "(CAST(oei.OEORI_SttDat AS VARCHAR) || 'T' || CAST(oei.OEORI_SttTim AS VARCHAR)) mdate "
            "FROM OE_OrdItem oei "
            "INNER JOIN OE_Order oe ON oei.OEORI_OEORD_ParRef = oe.oeord_rowid and oei.oeori_categ_dr = 1 "
            "INNER JOIN OEC_OrderStatus oes ON  oes.ostat_rowid = oei.OEORI_ItemStat_DR "
            "INNER JOIN PA_Adm pa ON  pa.PAADM_RowID = oe.OEORD_ADM_DR "
            f"WHERE  oes.OSTAT_Code in('E','V') AND oei.OEORI_SttDat >= '{date}'")

        result = self.query(query)
        return result if result else None

