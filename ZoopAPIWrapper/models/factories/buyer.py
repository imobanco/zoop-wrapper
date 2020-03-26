from ZoopAPIWrapper.models.buyer import Buyer
from ZoopAPIWrapper.models.factories.base import (
    ZoopMarketPlaceModelFactory, OwnerModelFactory, SocialModelFactory, FinancialModelFactory)


class BuyerFactory(ZoopMarketPlaceModelFactory, OwnerModelFactory,
                   SocialModelFactory, FinancialModelFactory):
    class Meta:
        model = Buyer

    resource = 'buyer'

    default_receipt_delivery_method = None
