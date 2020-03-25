from ZoopAPIWrapper.models.base import ZoopModel


class Token(ZoopModel):
    """
    Token is a resource used to link a BankAccount Or Card and a Customer
    https://docs.zoop.co/reference#token-1

    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        type: bank_account or card
        used: boolean of verification
    """
    RESOURCE = 'token'

    __FIELDS = ['type', 'used']

    def __init__(self, type, used, **kwargs):
        super().__init__(**kwargs)

        self.type = type
        self.used = used

    @property
    def fields(self):
        """
        the fields of ZoopBase are it's
        __FIELDS extended with it's father fields.
        it's important to be a new list (high order function)
        Returns: new list of attributes
        """
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)
