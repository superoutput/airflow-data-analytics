from hms_workflow_platform.core.queries.base.base_query import *


class PayorQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()

    def payor_create(self, date):
        collection = 'payors'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "org.code": self._site,
                    "statusflag": "A",
                    "modifiedat": {"$gte": date}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "code": "$code",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedat", "timezone": "+07:00",
                                          "onNull": ""}},
                }
            }
        ])
        
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None

    def payor_update(self, date):
        collection = 'tpas'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "org.code": self._site,
                    "statusflag": "A",
                    "modifiedat": {"$gte": date}
                }
            },
            {"$lookup": {"from": "payors", "localField": "payoruid", "foreignField": "_id", "as": "payors"}},
            {"$unwind": {"path": "$payors", "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 0,
                    "code": "$payors.code",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedat", "timezone": "+07:00",
                                          "onNull": ""}},
                }
            }
        ])
        
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None
