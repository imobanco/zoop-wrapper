class ZoopBase:
    __FIELDS = []

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def _from_dict(cls, **entries):
        return cls(**entries)

    @classmethod
    def from_dict(cls, data):
        try:
            return cls._from_dict(**data)
        except TypeError as e:
            print(e)
            return None

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

    def __init__(self, id=None, resource=None, uri=None,
                 created_at=None, updated_at=None,
                 metadata=None, **kwargs):
        super().__init__(**kwargs)
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

    def __init__(self, marketplace_id=None, **kwargs):
        super().__init__(**kwargs)

        self.marketplace_id = marketplace_id

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class Address(ZoopBase):
    __FIELDS = ["line1", "line2", "line3",
                "neighborhood", "city", "state",
                "postal_code", "country_code"]

    def __init__(self, line1, line2, line3,
                 neighborhood, city, state,
                 postal_code, country_code, **kwargs):
        super().__init__(**kwargs)

        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country_code = country_code

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)
