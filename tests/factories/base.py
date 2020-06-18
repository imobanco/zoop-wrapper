from factory import Factory, SubFactory, LazyFunction
from factory.faker import Faker
from pycpfcnpj import gen

from zoop_wrapper.models.base import (
    Address,
    FinancialModel,
    MarketPlaceModel,
    PaymentMethod,
    Person,
    ResourceModel,
    SocialModel,
    VerificationModel,
    ZoopObject,
)


class ZoopObjectFactory(Factory):
    """
    Factory for instances.
    The Meta.model dictates which instance to be created
    """

    class Meta:
        model = ZoopObject


class ResourceModelFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = ResourceModel

    created_at = Faker("date_of_birth")
    id = Faker("uuid4")
    metadata = {}
    resource = "resource"
    updated_at = Faker("date_this_month")
    uri = Faker("uri")


class MarketPlaceModelFactory(ResourceModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = MarketPlaceModel

    marketplace_id = Faker("uuid4")


class AddressFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = Address

    city = Faker("city")
    country_code = Faker("country_code", representation="alpha-2")
    line1 = Faker("street_name")
    line2 = Faker("building_number")
    line3 = Faker("secondary_address")
    neighborhood = Faker("street_suffix")
    postal_code = Faker("postalcode")
    state = Faker("military_state")


class PersonFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = Person

    address = SubFactory(AddressFactory)
    birthdate = Faker("date_of_birth")
    email = Faker("safe_email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    phone_number = Faker("phone_number")
    taxpayer_id = LazyFunction(gen.cpf)


class SocialModelFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = SocialModel

    facebook = Faker("uri")
    twitter = Faker("uri")


class FinancialModelFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = FinancialModel

    account_balance = Faker("pyfloat", positive=True, min_value=0.0)
    current_balance = Faker("pyfloat", positive=True, min_value=0.0)
    default_credit = Faker("pybool")
    default_debit = Faker("pybool")
    delinquent = Faker("pybool")
    description = Faker("sentence", nb_words=5)
    payment_methods = None
    status = Faker("random_element", elements=["active", "pending"])


class VerificationModelFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = VerificationModel

    address_line1_check = Faker("pybool")
    postal_code_check = Faker("pybool")


class PaymentMethodFactory(ResourceModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = PaymentMethod

    address = SubFactory(AddressFactory)
    customer = Faker("uuid4")
    description = Faker("sentence", nb_words=5)
