from factory.faker import Faker

from ZoopAPIWrapper.models.token import Token
from ZoopAPIWrapper.models.factories.base import (
    ZoopModelFactory)


class TokenFactory(ZoopModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = Token

    resource = 'token'

    type = Faker('random_element', elements=['card', 'bank_account'])
    used = Faker('pybool')
