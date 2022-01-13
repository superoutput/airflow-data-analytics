from hms_workflow_platform.core.queries.base.base_query import *


class PatientQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()
        self._site = site.upper()

    def patient_registration(self, date):
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
            {"$lookup": {"from": "patients", "localField": "patientuid", "foreignField": "_id", "as": "p"}},
            {
                "$project": {
                    "_id": 0,
                    "en": "$visitid",
                    "hn": {"$arrayElemAt": ["$p.mrn", 0]},
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedat", "timezone": "+07:00",
                                          "onNull": ""}},
                    "visit_status_id": {"$toString": "$visitstatusuid"},
                    "visitjourneys_modify": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": {"$max": "$visitjourneys.modifiedat"},
                                          "timezone": "+07:00", "onNull": ""}}
                }
            }
        ])
        
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None

    def patient_create(self, date):
        collection = 'patients'
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
                    "hn": "$mrn",
                    "mdate": {
                        "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedat", "timezone": "+07:00",
                                          "onNull": ""}}
                }
            }
        ])

        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None
