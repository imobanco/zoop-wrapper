from ZoopAPIWrapper.models.buyer import Buyer
from ZoopAPIWrapper.models.factories.base import (
    MarketPlaceModelFactory, PersonFactory,
    SocialModelFactory, FinancialModelFactory)


class BuyerFactory(MarketPlaceModelFactory, PersonFactory,
                   SocialModelFactory, FinancialModelFactory):
    class Meta:
        model = Buyer

    resource = 'buyer'

    default_receipt_delivery_method = None
