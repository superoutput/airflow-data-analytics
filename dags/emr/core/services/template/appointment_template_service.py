from hms_workflow_platform.core.services.base.base_service import BaseService


class AppointmentTemplateService(BaseService):

    def __init__(self):
        super().__init__()
        self._template = None

    def prepareTemplate(self, his):
        super().prepareTemplate(his)

    def generateKey(self, list_data):
        keys = self._template.appointment_default(list_data)
        new_keys = self.done_list(keys)
        return new_keys
