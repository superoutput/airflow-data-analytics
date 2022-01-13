
class PayorTemplate:

    def __init__(self):
        super().__init__()

    def payor_default(self, data_list):
        keys = []
        for data in data_list:
            key = f"{data.get('code')},{data.get('mdate')}"
            keys.append(key)

        return keys
