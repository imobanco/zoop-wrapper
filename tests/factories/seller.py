from factory import SubFactory, LazyFunction
from factory.faker import Faker
from pycpfcnpj import gen

from zoop_wrapper.models.seller import Seller
from tests.factories.base import (
    AddressFactory,
    FinancialModelFactory,
    MarketPlaceModelFactory,
    PersonFactory,
    SocialModelFactory,
)


class SellerFactory(MarketPlaceModelFactory, FinancialModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = Seller

    decline_on_fail_security_code = Faker("pybool")
    decline_on_fail_zipcode = Faker("pybool")
    is_mobile = Faker("pybool")
    mcc = None
    merchant_code = None
    resource = "seller"
    show_profile_online = Faker("pybool")
    statement_descriptor = None
    terminal_code = None
    type = None


class IndividualSellerFactory(SellerFactory, PersonFactory, SocialModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = Seller

    website = Faker("uri")
    type = "individual"


class BusinessSellerFactory(SellerFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """

    class Meta:
        model = Seller

    business_address = SubFactory(AddressFactory)
    business_description = Faker("sentence", nb_words=5)
    business_email = Faker("safe_email")
    business_facebook = Faker("uri")
    business_name = Faker("company")
    business_opening_date = Faker("date_this_month")
    business_phone = Faker("phone_number")
    business_twitter = Faker("uri")
    business_website = Faker("uri")
    ein = LazyFunction(gen.cnpj)
    owner = SubFactory(PersonFactory)
    type = "business"
