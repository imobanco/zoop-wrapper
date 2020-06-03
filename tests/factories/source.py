from factory import SubFactory
from factory.faker import Faker

from tests.factories.base import ZoopObjectFactory, ResourceModelFactory
from tests.factories.invoice import InvoiceFactory
from tests.factories.card import CardFactory
from zoop_wrapper.models.transaction import Source
from zoop_wrapper.models.transaction import PointOfSale, History, Transaction


class SourceCardPresentFactory(ZoopObjectFactory):
    class Meta:
        model = Source

    card = SubFactory(CardFactory)
    type = "card"
    currency = "BRL"
    usage = "single_use"
    amount = Faker("pyfloat", positive=True, max_value=999999)


class SourceCardNotPresentFactory(ZoopObjectFactory):
    class Meta:
        model = Source

    card = SubFactory(CardFactory)
    type = "card"
