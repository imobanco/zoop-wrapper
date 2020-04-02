from ZoopAPIWrapper.models.buyer import Buyer
from tests.factories.base import (
    MarketPlaceModelFactory, PersonFactory,
    SocialModelFactory, FinancialModelFactory)


class BuyerFactory(MarketPlaceModelFactory, PersonFactory,
                   SocialModelFactory, FinancialModelFactory):
    class Meta:
        model = Buyer

    resource = 'buyer'

    default_receipt_delivery_method = None
