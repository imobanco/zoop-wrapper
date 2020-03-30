from ZoopAPIWrapper.models.base import (
    MarketPlaceModel, Person, SocialModel, FinancialModel)


class Buyer(MarketPlaceModel, Person, SocialModel, FinancialModel):
    """
    Represent a buyer.
    https://docs.zoop.co/reference#comprador-1

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        default_receipt_delivery_method: ?
    """
    RESOURCE = 'buyer'

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {'default_receipt_delivery_method'}
        )
