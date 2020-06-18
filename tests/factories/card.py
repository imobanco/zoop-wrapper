from factory import SubFactory
from factory.faker import Faker

from zoop_wrapper.models.card import CardVerificationChecklist, Card
from tests.factories.base import VerificationModelFactory, PaymentMethodFactory


class CardVerificationChecklistFactory(VerificationModelFactory):
    class Meta:
        model = CardVerificationChecklist

    security_code_check = "fail"


class CardFactory(PaymentMethodFactory):
    class Meta:
        model = Card

    card_brand = Faker("company")
    expiration_month = Faker("pyint", min_value=1, max_value=12, step=1)
    expiration_year = Faker("pyint", min_value=2000, max_value=2030, step=1)
    fingerprint = Faker("uuid4")
    first4_digits = Faker("pyint", min_value=1000, max_value=9999, step=1)
    holder_name = Faker("name")
    is_active = Faker("pybool")
    is_valid = Faker("pybool")
    is_verified = Faker("pybool")
    last4_digits = Faker("pyint", min_value=1000, max_value=9999, step=1)
    resource = "card"
    verification_checklist = SubFactory(CardVerificationChecklistFactory)
