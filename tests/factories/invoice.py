from factory import SubFactory
from factory.faker import Faker

from zoop_wrapper.models.invoice import (
    BillingConfiguration,
    BillingInstructions,
    Invoice,
)
from tests.factories.base import ZoopObjectFactory, PaymentMethodFactory


class BillingConfigurationFactory(ZoopObjectFactory):
    class Meta:
        model = BillingConfiguration

    mode = None
    is_discount = None


class FeeFactory(BillingConfigurationFactory):
    is_discount = False
    start_date = Faker("date_this_month")


class DiscountFactory(BillingConfigurationFactory):
    is_discount = True
    limit_date = Faker("date_this_month")


class PercentFeeFactory(FeeFactory):
    mode = Faker("random_element", elements=BillingConfiguration.PERCENT_MODES)
    percentage = Faker("pyfloat", positive=True, max_value=99)


class FixedFeeFactory(FeeFactory):
    mode = BillingConfiguration.FIXED_MODE
    amount = Faker("pyfloat", positive=True, max_value=99)


class PercentDiscountFactory(DiscountFactory):
    mode = Faker("random_element", elements=BillingConfiguration.PERCENT_MODES)
    percentage = Faker("pyfloat", positive=True, max_value=99)


class FixedDiscountFactory(DiscountFactory):
    mode = BillingConfiguration.FIXED_MODE
    amount = Faker("pyfloat", positive=True, max_value=99)


class BillingInstructionsFactory(ZoopObjectFactory):
    class Meta:
        model = BillingInstructions

    discount = SubFactory(FixedDiscountFactory)
    interest = SubFactory(PercentFeeFactory)
    late_fee = SubFactory(FixedFeeFactory)


class InvoiceFactory(PaymentMethodFactory):
    class Meta:
        model = Invoice

    accepted = Faker("pybool")
    bank_code = Faker("pyint")
    barcode = Faker("pyint")
    billing_instructions = SubFactory(BillingInstructionsFactory)
    body_instructions = ["pague este boleto!"]
    document_number = Faker("pyint")
    downloaded = Faker("pybool")
    expiration_date = Faker("date_this_month")
    fingerprint = Faker("uuid4")
    paid_at = Faker("date_this_month")
    payment_limit_date = Faker("date_this_month")
    printed = Faker("pybool")
    recipient = Faker("company")
    reference_number = Faker("pyint")
    resource = "boleto"
    sequence = Faker("pyint")
    status = "not_paid"
    url = Faker("uri")
    zoop_boleto_id = Faker("uuid4")
