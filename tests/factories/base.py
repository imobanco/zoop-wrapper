from factory import Factory, SubFactory, LazyFunction
from factory.faker import Faker
from pycpfcnpj import gen

from zoop_wrapper.models.base import (
    ZoopObject,
    ResourceModel,
    MarketPlaceModel,
    Person,
    Address,
    SocialModel,
    FinancialModel,
    VerificationModel,
    PaymentMethod,
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

    id = Faker("uuid4")
    resource = "resource"
    uri = Faker("uri")
    created_at = Faker("date_of_birth")
    updated_at = Faker("date_this_month")
    metadata = {}


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

    line1 = Faker("street_name")
    line2 = Faker("building_number")
    line3 = Faker("secondary_address")
    neighborhood = Faker("street_suffix")
    city = Faker("city")
    state = Faker("military_state")
    postal_code = Faker("postalcode")
    country_code = Faker("country_code", representation="alpha-2")


class PersonFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = Person

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("safe_email")
    taxpayer_id = LazyFunction(gen.cpf)
    phone_number = Faker("phone_number")
    birthdate = Faker("date_of_birth")
    address = SubFactory(AddressFactory)


class SocialModelFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = SocialModel

    twitter = Faker("uri")
    facebook = Faker("uri")


class FinancialModelFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = FinancialModel

    status = Faker("random_element", elements=["active", "pending"])
    account_balance = Faker("pyfloat", positive=True, min_value=0.0)
    current_balance = Faker("pyfloat", positive=True, min_value=0.0)
    description = Faker("sentence", nb_words=5)
    delinquent = Faker("pybool")
    default_debit = Faker("pybool")
    default_credit = Faker("pybool")
    payment_methods = None


class VerificationModelFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = VerificationModel

    postal_code_check = Faker("pybool")
    address_line1_check = Faker("pybool")


class PaymentMethodFactory(ZoopObjectFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = PaymentMethod

    description = Faker("sentence", nb_words=5)
    customer = Faker("uuid4")
    address = SubFactory(AddressFactory)
