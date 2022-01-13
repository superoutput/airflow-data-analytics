
class EncounterTemplate:

    def __init__(self):
        super().__init__()

    def encounter_default(self, data_list):
        keys = []
        for data in data_list:
            key = f"{data.get('en')},{data.get('mdate')}"
            keys.append(key)

        return keys

    