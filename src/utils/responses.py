from datetime import datetime


class BasicResponse:
    __slots__ = ['status', 'payload', 'timestamp']

    def __init__(self):
        self.timestamp = str(datetime.now())

    def to_dict(self):
        d = {}
        for field in self.__slots__:
            val = getattr(self, field)
            if type(val) == dict:
                val = self._process_datetime(val)
            d[field] = val
        return d

    def _process_datetime(self, data):
        d = {}
        for k, v in data.items():
            if type(v) == datetime:
                d[k] = str(v)
            else:
                d[k] = v
        return d


class Error404Response(BasicResponse):

    def __init__(self, payload):
        super().__init__()
        self.status = 404
        self.payload = payload


class Ok20XResponse(BasicResponse):

    def __init__(self, payload):
        super().__init__()
        self.status = 200
        self.payload = payload
