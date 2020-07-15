from factory import SubFactory
from factory.faker import Faker

from tests.factories.base import ZoopObjectFactory, ResourceModelFactory
from tests.factories.invoice import InvoiceFactory
from tests.factories.card import CardFactory
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

    amount = Faker("pyfloat", positive=True, max_value=99)
    authorization_code = None
    authorization_nsu = None
    authorizer = None
    authorizer_id = None
    created_at = Faker("date_of_birth")
    gatewayResponseTime = None
    id = Faker("uuid4")
    operation_type = "created"
    response_code = None
    response_message = None
    status = "succeeded"
    transaction = Faker("uuid4")


class TransactionFactory(ResourceModelFactory):
    class Meta:
        model = Transaction

    amount = Faker("pyfloat", positive=True, max_value=99)
    app_transaction_uid = None
    business = None
    capture = Faker("pybool")
    captured = Faker("pybool")
    confirmed = "0"
    currency = "BRL"
    customer = Faker("uuid4")
    description = Faker("sentence", nb_words=5)
    discounts = None
    expected_on = Faker("date_this_month")
    fee_details = None
    fees = "0.0"
    gateway_authorizer = None
    history = SubFactory(HistoryFactory)
    individual = None
    installment_plan = None
    location_latitude = None
    location_longitude = None
    on_behalf_of = Faker("uuid4")
    original_amount = Faker("pyfloat", positive=True, max_value=99)
    point_of_sale = SubFactory(PointOfSaleFactory)
    pre_authorization = None
    reference_id = Faker("sentence", nb_words=5)
    refunded = Faker("pybool")
    refunds = None
    resource = "transaction"
    rewards = None
    sales_receipt = None
    statement_descriptor = Faker("sentence", nb_words=2)
    status = Faker("random_element", elements=["failed", "suceeded"])
    transaction_number = None
    voided = Faker("pybool")


class TransactionCreditFactory(TransactionFactory):
    class Meta:
        model = Transaction

    id = None
    payment_type = "credit"
    source = SubFactory(SourceCardPresentFactory)


class TransactionBoletoFactory(TransactionFactory):
    class Meta:
        model = Transaction

    payment_type = "boleto"

    payment_method = SubFactory(InvoiceFactory)


class CreateTransactionBoletoFactory(TransactionFactory):
    class Meta:
        model = Transaction

    id = None
    payment_method = SubFactory(InvoiceFactory)
    payment_type = "boleto"


class CancelTransactionCardFactory(TransactionFactory):
    class Meta:
        model = Transaction

    payment_method = SubFactory(CardFactory)
    payment_type = "credit"
    source = SubFactory(SourceCardPresentFactory)
