from factory import SubFactory, LazyFunction
from factory.faker import Faker
from pycpfcnpj import gen

from ZoopAPIWrapper.models.bank_account import (
    BankAccount, BankAccountVerificationModel
)
from ZoopAPIWrapper.models.factories.base import (
    MarketPlaceModelFactory, AddressFactory, VerificationModelFactory
)


class BankAccountVerificationModelFactory(VerificationModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = BankAccountVerificationModel

    deposit_check = Faker('pybool')


class BankAccountFactory(MarketPlaceModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = BankAccount

    resource = 'bank_account'

    holder_name = Faker('name')
    bank_code = Faker('pyint', min_value=0, max_value=999, step=1)
    routing_number = Faker('pyint', min_value=0, max_value=999999, step=1)
    account_number = Faker('pyint', min_value=0, max_value=999999, step=1)

    description = Faker('sentence', nb_words=5)
    bank_name = Faker('company')
    type = Faker('random_element', elements=['savings', 'checkings'])
    last4_digits = Faker('pyint', min_value=0, max_value=9999, step=1)
    country_code = Faker('country_code', representation='alpha-2')
    phone_number = Faker('phone_number')
    is_active = Faker('pybool')
    is_verified = Faker('pybool')
    debitable = Faker('pybool')
    customer = Faker('uuid4')
    fingerprint = Faker('uuid4')
    address = SubFactory(AddressFactory)
    verification_checklist = SubFactory(BankAccountVerificationModelFactory)


class BusinessBankAccountFactory(BankAccountFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = BankAccount

    ein = LazyFunction(gen.cnpj)


class IndividualBankAccountFactory(BankAccountFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = BankAccount

    taxpayer_id = LazyFunction(gen.cpf)
