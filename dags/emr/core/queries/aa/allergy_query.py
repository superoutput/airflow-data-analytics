from hms_workflow_platform.core.queries.base.base_query import *


class AllergyQuery(BaseQuery):

    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()

    def allergy_create(self, date):
        collection = 'allergies'
        query = ([
            {"$lookup": {"from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org"}},
            {
                "$match": {
                    "org.code": self._site,
                    "modifiedat": {"$gte": date}
                }
            },
            {"$unwind": {"path": "$drugallergies", "preserveNullAndEmptyArrays": True}},
            {"$unwind": {"path": "$foodallergies", "preserveNullAndEmptyArrays": True}},
            {"$unwind": {"path": "$otherallergies", "preserveNullAndEmptyArrays": True}},
            {
                "$match": {
                    "$or": [
                        {"drugallergies.createdon": {"$gte": date}},
                        {"foodallergies.createdon": {"$gte": date}},
                        {"otherallergies.createdon": {"$gte": date}}
                    ]
                }
            },
            {"$lookup": {"from": "patients", "localField": "patientuid", "foreignField": "_id", "as": "patients"}},
            {"$unwind": {"path": '$patients', "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 0,
                    "hn": "$patients.mrn",
                    "mdate": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {"$gte": ["$drugallergies.createdon", "$convertdate"]},
                                    "then": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S",
                                                               "date": "$drugallergies.createdon", "timezone": "+07:00",
                                                               "onNull": ""}},
                                },
                                {
                                    "case": {"$gte": ["$foodallergies.createdon", "$convertdate"]},
                                    "then": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S",
                                                               "date": "$foodallergies.createdon", "timezone": "+07:00",
                                                               "onNull": ""}},
                                },
                                {
                                    "case": {"$gte": ["$otherallergies.createdon", "$convertdate"]},
                                    "then": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S",
                                                               "date": "$otherallergies.createdon",
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
        return result if result else None
