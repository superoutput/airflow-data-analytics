from hms_workflow_platform.core.queries.base.base_query import *


class PractitionerQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()
        self._site = site.upper()

    def practitioner_create(self, date):
        collection = 'users'
        query = ([
            {"$lookup": {"from":"organisations","localField":"orguid","foreignField":"_id","as":"org"}},
            {"$match": {
                "org.code": self._site,
                "statusflag": "A"}
            },
            {
                "$project": {
                    "_id": 0,
                    "rowid": {
                        "$toString": "$_id"
                    },
                    'employee_id': "$code"
                }
            }
        ])

        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None


    def practitioner_update(self, date):
        collection = 'users'
        query = ([
            { "$lookup": { "from": "organisations", "localField": "orguid", "foreignField": "_id", "as": "org" } },
            {
                "$match": {
                    "org.code": self._site,
                    "statusflag": "A",
                    "modifiedat": { "$gte": date }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "rowid": {
                        "$toString": "$_id"
                    },
                    "employee_id": "$code",
                    "mdate": { "$dateToString": { "format": "%Y-%m-%dT%H:%M:%S", "date": "$modifiedat", "timezone": "+07:00", "onNull": "" } },
                }
            }
        ])
        
        result = [i for i in self.adapter.aggregate(collection=collection, pipeline=query)]
        return result if result else None
