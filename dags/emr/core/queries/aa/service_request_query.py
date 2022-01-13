from hms_workflow_platform.core.queries.base.base_query import *


class ServiceRequestQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()

    def service_request_create(self, date):
        collection = 'patientorders'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "org.code": self._site,
                    "statusflag": "A",
                    "ordercattype": {"$ne": "MEDICINE"},
                    "modifiedat": {"$gte": date}
                }
            },
            {"$lookup": {"from": "patientvisits", "localField": "patientvisituid", "foreignField": "_id", "as": "pv"}},
            {"$unwind": {"path": "$pv", "preserveNullAndEmptyArrays": False}},
            {
                "$group": {
                    "_id": "$pv.visitid", "modifiedate": {"$max": "$modifiedat"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "en": "$_id",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedate", "timezone": "+07:00",
                                          "onNull": ""}}
                }
            }
        ])

        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None
        

    def service_request_update(self, date):
        collection = 'patientorders'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {"$match": {"org.code": self._site, "statusflag": "A", "ordercattype": {"$ne": "MEDICINE"},
                        "modifiedat": {"$gte": date}}},
            {
                "$unwind": {
                    "path": "$patientorderitems",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$unwind": {
                    "path": "$patientorderitems.patientorderlogs",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {"$match": {"patientorderitems.patientorderlogs.modifiedat": {"$gte": date}}},
            {"$lookup": {"from": "patientvisits", "localField": "patientvisituid", "foreignField": "_id", "as": "pv"}},
            {"$unwind": {"path": "$pv", "preserveNullAndEmptyArrays": False}},
            {
                "$group": {
                    "_id": "$pv.visitid", "modifiedate": {"$max": "$patientorderitems.patientorderlogs.modifiedat"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "en": "$_id",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedate", "timezone": "+07:00",
                                          "onNull": ""}}
                }
            }
        ])

        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None
        
