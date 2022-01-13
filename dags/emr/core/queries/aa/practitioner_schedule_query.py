from hms_workflow_platform.core.queries.base.base_query import *


class PractitionerScheduleQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()

    def practitioner_schedule_create(self, site, date, tomorrow):
        collection = 'appointmentschedules'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "org.code": self._site,
                    "$or": [
                        {"$and": [
                            {"appointmentdate": {"$gte": date}},
                            {"appointmentdate": {"$lt": tomorrow}}
                        ]
                        },
                        {"$and": [
                            {"modifiedat": {"$gte": date}},
                            {"modifiedat": {"$lt": tomorrow}}]
                        }
                    ]
                }
            },
            {"$lookup": {"from": "users", "localField": "careprovideruid", "foreignField": "_id", "as": "users"}},
            {"$unwind": {"path": "$users", "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 0,
                    "code": "$users.code",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedat", "timezone": "+07:00",
                                          "onNull": ""}},
                    "appointmentdate": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$appointmentdate",
                                                          "timezone": "+07:00", "onNull": ""}}
                }
            }
        ])
        
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None
