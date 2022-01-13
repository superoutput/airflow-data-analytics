from hms_workflow_platform.core.queries.base.base_query import *


class PatientQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self.adapter = self.get_adapter(site)
        self.query = self.adapter.query
        self._site = site

    def patient_registration(self, date):
        query = (
            "SELECT PAADM_ADMNo en, PA_Patmas.PAPMI_NO hn, "
            "(CAST(PAADM_UpdateDate AS VARCHAR) || 'T' || CAST(PAADM_UpdateTime AS VARCHAR)) mdate "
            "FROM PA_Adm "
            "LEFT JOIN PA_Patmas ON PA_Patmas.PAPMI_Rowid = PA_Adm.PAADM_PAPMI_DR "
            f"WHERE PAADM_UpdateDate >= '{date}' AND PAADM_ADMNo IS NOT NULL "
            "ORDER BY mdate")

        result = self.query(query)
        return result if result else None

    def patient_create(self, date):
        query = (
            "SELECT PA_Patmas.PAPMI_NO hn, "
            "(CAST(PA_Person.PAPER_UpdateDate AS VARCHAR) || 'T' || CAST(PA_Person.PAPER_UpdateTime AS VARCHAR)) mdate "
            "FROM PA_Patmas "
            "LEFT JOIN PA_Person ON PA_Person.PAPER_PAPMI_DR = PA_Patmas.PAPMI_Rowid "
            f"WHERE PA_Person.PAPER_UpdateDate >= '{date}' "
            "AND PA_Patmas.PAPMI_NO IS NOT NULL "
            "ORDER BY mdate")

        result = self.query(query)
        return result if result else None

    def patient_update(self, date):
        query = (
            "SELECT papam.papmi_no hn, "
            "(CAST(paper.PAPER_UpdateDate AS VARCHAR) || 'T' || CAST(paper.PAPER_UpdateTime AS VARCHAR)) mdate "
            "FROM PA_Person paper "
            "INNER JOIN PA_PatMas papam ON papam.PAPMI_RowId = paper.PAPER_PAPMI_DR "
            f"WHERE paper.PAPER_UpdateDate >= '{date}'")

        result = self.query(query)
        return result if result else None

