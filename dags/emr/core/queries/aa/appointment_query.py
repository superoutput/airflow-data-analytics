from hms_workflow_platform.core.queries.base.base_query import *


class AppointmentQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()

    def appointment_create(self, date):
        collection = 'appointmentschedules'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "org.code": self._site,
                    "appointmentdate": {"$gte": date},
                    "slots": {"$ne": []}
                },
            },
            {"$lookup": {"from": "patients", "localField": "slots.patientuid", "foreignField": "_id", "as": "p"}},
            {"$unwind": {"path": "$p", "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 0,
                    "hn": "$p.mrn",
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