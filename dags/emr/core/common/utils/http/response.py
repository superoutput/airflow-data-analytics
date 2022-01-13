class Response:
    def __init__(self, message=None, data=None):
        self.message = message
        self.data = data

    def build(self):
        return {
            "message": self.message,
            "data": self.data
        }
