from pytz import timezone
from hms_workflow_platform.core.queries.base.base_query import *
import datetime


class VitalSignQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query

    def vitalsign_create(self, date):
        ten_days_ago_date = self.ten_days_ago()
        query = ("SELECT DISTINCT pa.paadm_admno en, "
                 "(CAST(ob.OBS_Date AS VARCHAR) || 'T' || CAST(ob.OBS_Time AS VARCHAR)) mdate "
                 "FROM PA_Adm pa "
                 "INNER JOIN MR_Observations ob ON ob.OBS_ParRef = pa.paadm_mainmradm_dr "
                 "INNER JOIN MRC_ObservationItem obi ON obi.ITM_RowId = ob.OBS_Item_DR "
                 "WHERE pa.PAADM_ADMNo IS NOT NULL AND obi.itm_code IN ('VS1','VS2','VS3','VS4','VS5','VS6','HEIGHT','WEIGHT') "
                 f"AND pa.PAADM_UpdateDate >= '{ten_days_ago_date}' AND ob.OBS_Date >= '{date}'")

        result = self.query(query)
        return result if result else None
