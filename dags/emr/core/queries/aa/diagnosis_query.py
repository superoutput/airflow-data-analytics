from hms_workflow_platform.core.queries.base.base_query import *


class DiagnosisQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()

    def diagnostic_create(self, date):
        collection = 'diagnoses'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "org.code": self._site,
                    "diagnosis.isactive": {"$eq": True},
                    "modifiedat": {"$gte": date}
                }
            },
            {"$unwind": {"path": "$diagnosis", "preserveNullAndEmptyArrays": True}},
            {"$lookup": {"from": "patientvisits", "localField": "patientvisituid", "foreignField": "_id", "as": "pv"}},
            {"$unwind": {"path": "$pv", "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 0,
                    "en": "$pv.visitid",
                    "mdate": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {"$gte": ["$diagnosis.createdat", "$convertdate"]},
                                    "then": {
                                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$diagnosis.createdat",
                                                          "timezone": "+07:00", "onNull": ""}},
                                },
                                {
                                    "case": {"$gte": ["$modifiedat", "$convertdate"]},
                                    "then": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedat",
                                                               "timezone": "+07:00", "onNull": ""}},
                                }
                            ],
                            "default": ""
                        }
                    }
                }
            }
        ])
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        print(result)
        return result if result else None        
