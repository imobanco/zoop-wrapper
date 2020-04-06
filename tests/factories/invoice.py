from factory import SubFactory
from factory.faker import Faker

from ZoopAPIWrapper.models.invoice import (
    BillingConfiguration, BillingInstructions, Invoice
)
from tests.factories.base import (
    ZoopObjectFactory, PaymentMethodFactory
)


class BillingConfigurationFactory(ZoopObjectFactory):
    class Meta:
        model = BillingConfiguration

    mode = None
    is_discount = None


class FeeFactory(BillingConfigurationFactory):
    is_discount = False
    start_date = Faker('date_this_month')


class DiscountFactory(BillingConfigurationFactory):
    is_discount = True
    limit_date = Faker('date_this_month')


class PercentFeeFactory(FeeFactory):
    mode = Faker('random_element', elements=BillingConfiguration.PERCENT_MODES)
    percentage = Faker('pyfloat', positive=True, max_value=99)


class FixedFeeFactory(FeeFactory):
    mode = BillingConfiguration.FIXED_MODE
    amount = Faker('pyfloat', positive=True, max_value=99)


class PercentDiscountFactory(DiscountFactory):
    mode = Faker('random_element', elements=BillingConfiguration.PERCENT_MODES)
    percentage = Faker('pyfloat', positive=True, max_value=99)


class FixedDiscountFactory(DiscountFactory):
    mode = BillingConfiguration.FIXED_MODE
    amount = Faker('pyfloat', positive=True, max_value=99)


class BillingInstructionsFactory(ZoopObjectFactory):
    class Meta:
        model = BillingInstructions

    late_fee = SubFactory(FixedFeeFactory)
    interest = SubFactory(PercentFeeFactory)
    discount = SubFactory(FixedDiscountFactory)


class InvoiceFactory(PaymentMethodFactory):
    class Meta:
        model = Invoice

    expiration_date = Faker('date_this_month')

    zoop_boleto_id = Faker('uuid4')
    status = 'not_paid'
    reference_number = Faker('pyint')
    document_number = Faker('pyint')
    recipient = Faker('company')
    bank_code = Faker('pyint')
    sequence = Faker('pyint')
    url = Faker('uri')
    accepted = Faker('pybool')
    printed = Faker('pybool')
    downloaded = Faker('pybool')
    fingerprint = Faker('uuid4')
    paid_at = Faker('date_this_month')
    barcode = Faker('pyint')
    payment_limit_date = Faker('date_this_month')
    body_instructions = ['pague este boleto!']
    billing_instructions = SubFactory(BillingInstructionsFactory)
