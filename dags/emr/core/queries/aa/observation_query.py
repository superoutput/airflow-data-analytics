from hms_workflow_platform.core.queries.base.base_query import *


class ObservationQuery(BaseQuery):
    def __init__(self, site):
        super().__init__()
        self._site = site.upper()
        self.adapter = self.get_mongodb_commander()

    def observation_create(self, date):
        return None
