from factory import SubFactory
from factory.faker import Faker

from tests.factories.base import ZoopObjectFactory, ResourceModelFactory
from tests.factories.invoice import InvoiceFactory
from tests.factories.token import CreateCardTokenFactory
from zoop_wrapper.models.transaction import Source
from zoop_wrapper.models.transaction import PointOfSale, History, Transaction


class SourceCardPresentFactory(ZoopObjectFactory):
    class Meta:
        model = Source

    amount = Faker("pyfloat", positive=True, max_value=999999)
    card = SubFactory(CreateCardTokenFactory)
    currency = "BRL"
    type = "card"
    usage = "single_use"


class SourceCardNotPresentFactory(ZoopObjectFactory):
    class Meta:
        model = Source

    card = SubFactory(CreateCardTokenFactory)
    type = "card"
