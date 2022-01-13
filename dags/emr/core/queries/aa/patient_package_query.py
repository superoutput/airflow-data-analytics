from hms_workflow_platform.core.queries.base.base_query import *


class PatientPackageQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()

    def patient_packages_create(self, date):
        collection = 'patientpackages'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "org.code": self._site,
                    "statusflag": "A",
                    "modifiedat": {"$gte": date}
                }
            },
            {"$lookup": {"from": "patientvisits", "localField": "patientvisituid", "foreignField": "_id", "as": "pv"}},
            {"$unwind": {"path": "$pv", "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 0,
                    "en": "$pv.visitid",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedat", "timezone": "+07:00",
                                          "onNull": ""}},
                }
            }
        ])
        
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None
