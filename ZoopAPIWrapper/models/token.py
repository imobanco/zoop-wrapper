from ZoopAPIWrapper.models.base import ZoopModel


class Token(ZoopModel):
    RESOURCE = 'token'

    __FIELDS = ['type', 'used']

    def __init__(self, type, used, **kwargs):
        super().__init__(**kwargs)

        self.type = type
        self.used = used

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)
