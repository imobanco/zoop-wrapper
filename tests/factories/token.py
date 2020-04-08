from factory import SubFactory, LazyFunction
from factory.faker import Faker
from pycpfcnpj import gen

from zoop_wrapper.models.token import Token
from tests.factories.base import (
    ResourceModelFactory)
from tests.factories.card import CardFactory
from zoop_wrapper.models.bank_account import BankAccount
from tests.factories.bank_account import IndividualBankAccountFactory


class TokenFactory(ResourceModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = Token

    resource = 'token'

    type = None
    used = Faker('pybool')


class CardTokenFactory(TokenFactory):
    type = 'card'

    card = SubFactory(CardFactory)


class CreateCardTokenFactory(TokenFactory):
    card_number = Faker('credit_card_number')
    security_code = Faker('credit_card_security_code')
    expiration_month = Faker('pyint', min_value=1, max_value=12, step=1)
    expiration_year = Faker('pyint', min_value=2000, max_value=2030, step=1)
    holder_name = Faker('name')


class BankAccountTokenFactory(TokenFactory):
    type = 'bank_account'

    bank_account = SubFactory(IndividualBankAccountFactory)


class CreateBankAccountTokenFactory(TokenFactory):
    type = Faker('random_element', elements=BankAccount.TYPES)
    holder_name = Faker('name')
    bank_code = Faker('pyint', min_value=0, max_value=999, step=1)
    routing_number = Faker('pyint', min_value=0, max_value=999999, step=1)
    account_number = Faker('pyint', min_value=0, max_value=999999, step=1)


class CreateIndividualBankAccountTokenFactory(CreateBankAccountTokenFactory):
    taxpayer_id = LazyFunction(gen.cpf)


class CreateBusinessBankAccountTokenFactory(CreateBankAccountTokenFactory):
    ein = LazyFunction(gen.cnpj)
