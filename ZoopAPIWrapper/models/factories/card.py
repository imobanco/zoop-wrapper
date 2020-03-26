from factory import SubFactory
from factory.faker import Faker

from ZoopAPIWrapper.models.card import (
    CardVerificationChecklist, Card
)
from ZoopAPIWrapper.models.factories.base import (
    VerificationCheckListFactory, PaymentMethodFactory
)


class CardVerificationChecklistFactory(VerificationCheckListFactory):
    class Meta:
        model = CardVerificationChecklist

    security_code_check = 'fail'


class CardFactory(PaymentMethodFactory):
    class Meta:
        model = Card

    resource = 'card'

    card_brand = Faker('company')
    first4_digits = Faker('pyint', min_value=1000, max_value=9999, step=1)
    last4_digits = Faker('pyint', min_value=1000, max_value=9999, step=1)
    expiration_month = Faker('pyint', min_value=1, max_value=12, step=1)
    expiration_year = Faker('pyint', min_value=2000, max_value=2030, step=1)
    holder_name = Faker('name')
    is_active = Faker('pybool')
    is_valid = Faker('pybool')
    is_verified = Faker('pybool')
    fingerprint = Faker('uuid4')
    verification_checklist = SubFactory(CardVerificationChecklistFactory)