from factory.faker import Faker

from ZoopAPIWrapper.models.token import Token
from tests.factories.base import (
    ResourceModelFactory)


class TokenFactory(ResourceModelFactory):
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
