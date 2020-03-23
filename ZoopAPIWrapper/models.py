
class ZoopBase:
    __FIELDS = []

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def _from_dict(cls, **entries):
        return cls(**entries)

    @classmethod
    def from_dict(cls, data):
        return cls._from_dict(**data)

    def to_dict(self):
        data = {}
        for field in self.fields:
            try:
                data[field] = self.__getattribute__(field).to_dict()
            except AttributeError:
                data[field] = self.__getattribute__(field)
        return data

    @property
    def fields(self):
        return list(self.__FIELDS)
