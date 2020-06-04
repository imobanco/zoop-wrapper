from factory import SubFactory
from factory.faker import Faker

from tests.factories.base import ZoopObjectFactory, ResourceModelFactory
from tests.factories.invoice import InvoiceFactory
from tests.factories.source import SourceCardPresentFactory
from zoop_wrapper.models.transaction import PointOfSale, History, Transaction


class PointOfSaleFactory(ZoopObjectFactory):
    class Meta:
        model = PointOfSale

    entry_mode = "barcode"
    identification_number = 123


class HistoryFactory(ZoopObjectFactory):
    class Meta:
        model = History

    id = Faker("uuid4")
    transaction = Faker("uuid4")
    amount = Faker("pyfloat", positive=True, max_value=99)
    operation_type = "created"
    status = "succeeded"
    response_code = None
    response_message = None
    authorization_code = None
    authorizer_id = None
    authorization_nsu = None
    gatewayResponseTime = None
    authorizer = None
    created_at = Faker("date_of_birth")


class TransactionFactory(ResourceModelFactory):
    class Meta:
        model = Transaction

    resource = "transaction"

    amount = Faker("pyfloat", positive=True, max_value=99)
    currency = "BRL"
    description = Faker("sentence", nb_words=5)
    reference_id = Faker("sentence", nb_words=5)
    on_behalf_of = Faker("uuid4")
    customer = Faker("uuid4")
    status = Faker("random_element", elements=["failed", "suceeded"])
    confirmed = "0"
    original_amount = Faker("pyfloat", positive=True, max_value=99)
    transaction_number = None
    gateway_authorizer = None
    app_transaction_uid = None
    refunds = None
    rewards = None
    discounts = None
    pre_authorization = None
    sales_receipt = None
    statement_descriptor = Faker("sentence", nb_words=2)
    installment_plan = None
    refunded = Faker("pybool")
    voided = Faker("pybool")
    captured = Faker("pybool")
    fees = "0.0"
    fee_details = None
    location_latitude = None
    location_longitude = None
    individual = None
    business = None
    expected_on = Faker("date_this_month")

    payment_type = "boleto"
    payment_method = SubFactory(InvoiceFactory)
    point_of_sale = SubFactory(PointOfSaleFactory)
    history = SubFactory(HistoryFactory)


class TransactionSource(TransactionFactory):
    class Meta:
        model = Transaction

    source = SubFactory(SourceCardPresentFactory)

class TransactionBoleto(TransactionFactory):
    class Meta:
        model = Transaction

    boleto = SubFactory(InvoiceFactory)
