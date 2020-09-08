from factory.faker import Faker

from tests.factories.base import ZoopObjectFactory
from zoop_wrapper.models.transaction import InstallmentPlan


class InstallmentPlanFactory(ZoopObjectFactory):
    class Meta:
        model = InstallmentPlan

    mode = Faker("random_element", elements=InstallmentPlan.INSTALLMENT_PLAN_MODES)
    number_installments = Faker("pyint", min_value=1, max_value=12, step=1)
