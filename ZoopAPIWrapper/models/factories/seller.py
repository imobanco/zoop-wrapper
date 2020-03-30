from factory import SubFactory, LazyFunction
from factory.faker import Faker
from pycpfcnpj import gen

from ZoopAPIWrapper.models.seller import Seller
from ZoopAPIWrapper.models.factories.base import (
    MarketPlaceModelFactory, PersonFactory,
    SocialModelFactory, FinancialModelFactory,
    AddressFactory
)


class SellerFactory(MarketPlaceModelFactory, FinancialModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = Seller

    resource = 'seller'

    statement_descriptor = None
    mcc = None
    show_profile_online = Faker('pybool')
    is_mobile = Faker('pybool')
    decline_on_fail_security_code = Faker('pybool')
    decline_on_fail_zipcode = Faker('pybool')
    merchant_code = None
    terminal_code = None
    type = None


class IndividualSellerFactory(SellerFactory, PersonFactory,
                              SocialModelFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = Seller

    website = Faker('uri')
    type = 'individual'


class BusinessSellerFactory(SellerFactory):
    """
    Factory for instances with fake attributes.
    The Meta.model dictates which instance to be created.

    https://faker.readthedocs.io/en/latest/providers.html
    """
    class Meta:
        model = Seller

    type = 'business'
    ein = LazyFunction(gen.cnpj)
    business_name = Faker('company')
    business_phone = Faker('phone_number')
    business_email = Faker('safe_email')
    business_website = Faker('uri')
    business_opening_date = Faker('date_this_month')
    business_address = SubFactory(AddressFactory)
    owner = SubFactory(PersonFactory)

    business_description = Faker('sentence', nb_words=5)
    business_facebook = Faker('uri')
    business_twitter = Faker('uri')
