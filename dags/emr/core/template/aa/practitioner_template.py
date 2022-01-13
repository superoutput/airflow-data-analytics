
class PractitionerTemplate:

    def __init__(self):
        super().__init__()

    def practitioner_default(self, data_list):
        keys = []
        for data in data_list:
            key = f"{data.get('rowid')},{data.get('employee_id')}"
            keys.append(key)

        return keys
