from factory.faker import Faker

from ZoopAPIWrapper.models.token import Token
from ZoopAPIWrapper.models.factories.base import (
    ZoopModelFactory)


class TokenFactory(ZoopModelFactory):
    class Meta:
        model = Token

    resource = 'token'

    type = Faker('random_element', elements=['card', 'bank_account'])
    used = Faker('pybool')
