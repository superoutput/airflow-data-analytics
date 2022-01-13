from hms_workflow_platform.core.queries.base.base_query import *


class EncounterQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()

    def encounter_create(self, date):
        collection = 'patientvisits'
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
                    "en": "$visitid",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedat", "timezone": "+07:00",
                                          "onNull": ""}},
                    "visit_status_id": {"$toString": "$visitstatusuid"}
                }
            }
        ])
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None

    def encounter_update(self, date):
        collection = 'patientvisits'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "enddate": None,
                    "org.code": self._site,
                    "statusflag": "A",
                    "visitjourneys.modifiedat": {"$gte": date}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "en": "$visitid",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": {"$max": "$visitjourneys.modifiedat"},
                                          "timezone": "+07:00", "onNull": ""}},
                    "visit_status_id": {"$toString": "$visitstatusuid"}
                }
            }
        ])
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None

    def encounter_discharge(self, date):
        collection = 'patientvisits'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "org.code": self._site,
                    "medicaldischargedate": {"$gte": date}
                }
            },
            {"$unwind": {"path": "$p", "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 0,
                    "en": "$visitid",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$medicaldischargedate",
                                          "timezone": "+07:00", "onNull": ""}
                    },
                }
            }
        ])
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None
