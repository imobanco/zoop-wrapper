from factory import Factory, SubFactory, LazyFunction
from factory.faker import Faker
from pycpfcnpj import gen

from ZoopAPIWrapper.models.base import (
    ZoopBase, ZoopModel, ZoopMarketPlaceModel,
    OwnerModel, AddressModel,
    SocialModel, FinancialModel,
    VerificationChecklist, PaymentMethod
)


class ZoopBaseFactory(Factory):
    """
    Factory for instances.
    The Meta.model dictates which instance to be created
    """
    class Meta:
        model = ZoopBase


class ZoopModelFactory(ZoopBaseFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = ZoopModel

    id = Faker('uuid4')
    resource = 'resource'
    uri = Faker('uri')
    created_at = Faker('date_of_birth')
    updated_at = Faker('date_this_month')
    metadata = {}


class ZoopMarketPlaceModelFactory(ZoopModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = ZoopMarketPlaceModel

    marketplace_id = Faker('uuid4')


class AddressModelFactory(ZoopBaseFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = AddressModel

    line1 = Faker('street_name')
    line2 = Faker('building_number')
    line3 = Faker('secondary_address')
    neighborhood = Faker('street_suffix')
    city = Faker('city')
    state = Faker('military_state')
    postal_code = Faker('postalcode')
    country_code = Faker('country_code', representation='alpha-2')


class OwnerModelFactory(ZoopBaseFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = OwnerModel

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('safe_email')
    taxpayer_id = LazyFunction(gen.cpf)
    phone_number = Faker('phone_number')
    birthdate = Faker('date_of_birth')
    address = SubFactory(AddressModelFactory)


class SocialModelFactory(ZoopBaseFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = SocialModel

    twitter = Faker('uri')
    facebook = Faker('uri')


class FinancialModelFactory(ZoopBaseFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = FinancialModel

    status = Faker('random_element', elements=['active', 'pending'])
    account_balance = Faker('pyfloat', positive=True, min_value=0.0)
    current_balance = Faker('pyfloat', positive=True, min_value=0.0)
    description = Faker('sentence', nb_words=5)
    delinquent = Faker('pybool')
    default_debit = Faker('pybool')
    default_credit = Faker('pybool')
    payment_methods = None


class VerificationCheckListFactory(ZoopBaseFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = VerificationChecklist

    postal_code_check = Faker('pybool')
    address_line1_check = Faker('pybool')


class PaymentMethodFactory(ZoopModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = PaymentMethod

    description = Faker('sentence', nb_words=5)
    customer = Faker('uuid4')
    address = SubFactory(AddressModelFactory)
