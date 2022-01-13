from hms_workflow_platform.core.queries.base.base_query import *


class CcQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()

    def cc_create(self, date):
        collection = 'cchpis'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "org.code": self._site,
                    "cchpis": {"$exists": True, "$ne": []},
                    "modifiedat": {"$gte": date}
                }
            },
            {"$lookup": {"from": "patientvisits", "localField": "patientvisituid", "foreignField": "_id", "as": "pv"}},
            {"$unwind": {"path": "$pv", "preserveNullAndEmptyArrays": False}},
            {
                "$project": {
                    "_id": 0,
                    "en": "$pv.visitid",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedat", "timezone": "+07:00",
                                          "onNull": ""}}
                }
            }
        ])
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None