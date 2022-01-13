
class AllergyTemplateService:

    def __init__(self):
        super().__init__()

    def allergy_default(self, data_list):
        keys = []
        for data in data_list:
            key = f"{data.get('hn')},{data.get('mdate')},{data.get('appointmentdate')}"
            keys.append(key)

        return keys
