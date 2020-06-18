from factory import SubFactory, LazyFunction
from factory.faker import Faker
from pycpfcnpj import gen

from zoop_wrapper.models.bank_account import BankAccount, BankAccountVerificationModel
from tests.factories.base import (
    MarketPlaceModelFactory,
    AddressFactory,
    VerificationModelFactory,
)


class BankAccountVerificationModelFactory(VerificationModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = BankAccountVerificationModel

    deposit_check = Faker("pybool")


class BankAccountFactory(MarketPlaceModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = BankAccount

    account_number = Faker("pyint", min_value=0, max_value=999999, step=1)
    address = SubFactory(AddressFactory)
    bank_code = Faker("pyint", min_value=0, max_value=999, step=1)
    bank_name = Faker("company")
    country_code = Faker("country_code", representation="alpha-2")
    customer = Faker("uuid4")
    debitable = Faker("pybool")
    description = Faker("sentence", nb_words=5)
    fingerprint = Faker("uuid4")
    holder_name = Faker("name")
    is_active = Faker("pybool")
    is_verified = Faker("pybool")
    last4_digits = Faker("pyint", min_value=1000, max_value=9999, step=1)
    phone_number = Faker("phone_number")
    resource = "bank_account"
    routing_number = Faker("pyint", min_value=0, max_value=999999, step=1)
    type = Faker("random_element", elements=BankAccount.TYPES)
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
