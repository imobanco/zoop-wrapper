from ZoopAPIWrapper.models.base import (
    ZoopMarketPlaceModel, OwnerModel, SocialModel, FinancialModel)


class Buyer(ZoopMarketPlaceModel, OwnerModel, SocialModel, FinancialModel):
    """
    Represent a buyer.
    https://docs.zoop.co/reference#comprador-1

    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        default_receipt_delivery_method: ?
    """
    RESOURCE = 'buyer'

    __FIELDS = ['default_receipt_delivery_method']

    def __init__(self, default_receipt_delivery_method=None,
                 **kwargs):
        super().__init__(**kwargs)

        self.default_receipt_delivery_method = default_receipt_delivery_method

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
