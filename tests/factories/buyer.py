from factory.faker import Faker
from factory import LazyFunction
from pycpfcnpj import gen

from zoop_wrapper.models.buyer import Buyer
from tests.factories.base import (
    FinancialModelFactory,
    MarketPlaceModelFactory,
    PersonFactory,
    SocialModelFactory,
)


class BuyerFactory(
    MarketPlaceModelFactory, PersonFactory, SocialModelFactory, FinancialModelFactory
):
    class Meta:
        model = Buyer

    resource = "buyer"
    taxpayer_id = LazyFunction(
        lambda: Faker(
            "random_element",
            elements=[
                gen.cpf(),
                gen.cnpj()]
        ).generate()
    )
    default_receipt_delivery_method = None
