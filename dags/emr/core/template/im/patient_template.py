
class PatientTemplate:

    def __init__(self):
        super().__init__()

    def patient_default(self, data_list):
        keys = []
        for data in data_list:
            key = f"{data.get('hn')},{data.get('mdate')}"
            keys.append(key)

        return keys

    