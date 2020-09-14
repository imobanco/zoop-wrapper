from factory import SubFactory
from factory.faker import Faker

from zoop_wrapper.models.invoice import (
    BaseModeObject,
    BillingInstructions,
    Discount,
    Fine,
    Interest,
    Invoice,
)
from tests.factories.base import ZoopObjectFactory, PaymentMethodFactory


class BaseModeObjectFactory(ZoopObjectFactory):
    class Meta:
        model = BaseModeObject

    mode = None


class FixedBaseModeObjectFactory(BaseModeObjectFactory):
    amount = Faker("pyfloat", positive=True, max_value=99)


class PercentageBaseModeObjectFactory(BaseModeObject):
    percentage = Faker("pyfloat", positive=True, max_value=99)


class FixedFineFactory(FixedBaseModeObjectFactory):
    class Meta:
        model = Fine

    mode = "FIXED"


class PercentageFineFactory(PercentageBaseModeObjectFactory):
    class Meta:
        model = Fine

    mode = "PERCENTAGE"


class FixedInterestFactory(FixedBaseModeObjectFactory):
    class Meta:
        model = Interest

    mode = "DAILY_AMOUNT"


class PercentageInterestFactory(PercentageBaseModeObjectFactory):
    class Meta:
        model = Interest

    mode = Faker(
        "random_element",
        elements=[Interest.DAILY_PERCENTAGE, Interest.MONTHLY_PERCENTAGE],
    )


class FixedDiscountFactory(FixedBaseModeObjectFactory):
    class Meta:
        model = Discount

    mode = "FIXED"
    limit_date = Faker("date_this_month")


class PercentageDiscountFactory(PercentageBaseModeObjectFactory):
    class Meta:
        model = Discount

    mode = "PERCENTAGE"
    limit_date = Faker("date_this_month")


class BillingInstructionsFactory(ZoopObjectFactory):
    class Meta:
        model = BillingInstructions

    discount = SubFactory(FixedDiscountFactory)
    interest = SubFactory(FixedInterestFactory)
    late_fee = SubFactory(FixedFineFactory)


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
