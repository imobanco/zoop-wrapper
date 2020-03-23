
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


class ZoopModel(ZoopBase):
    __FIELDS = ["id", "resource", "uri", "created_at", "updated_at", "metadata"]

    def __init__(self, id, resource, uri, created_at, updated_at, metadata):
        super().__init__()
        self.id = id
        self.resource = resource
        self.uri = uri

        self.created_at = created_at
        self.updated_at = updated_at
        self.metadata = metadata

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class ZoopMarketPlaceModel(ZoopModel):
    __FIELDS = ["marketplace_id"]

    def __init__(self, marketplace_id, **kwargs):
        super().__init__(**kwargs)

        self.marketplace_id = marketplace_id

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)

