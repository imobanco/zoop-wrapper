from factory import SubFactory
from factory.faker import Faker

from ZoopAPIWrapper.models.invoice import (
    BillingConfiguration, BillingInstructions
)
from ZoopAPIWrapper.models.factories.base import (
    ZoopObjectFactory,
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
