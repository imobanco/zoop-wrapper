from factory import SubFactory, LazyFunction
from factory.faker import Faker
from pycpfcnpj import gen

from ZoopAPIWrapper.models.seller import Seller, IndividualSeller, BusinessSeller
from ZoopAPIWrapper.models.factories.base import (
    ZoopMarketPlaceModelFactory, OwnerModelFactory,
    SocialModelFactory, FinancialModelFactory, AddressModelFactory
)


class SellerFactory(ZoopMarketPlaceModelFactory, FinancialModelFactory):
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


class IndividualSellerFactory(SellerFactory, OwnerModelFactory, SocialModelFactory):
    class Meta:
        model = IndividualSeller

    website = Faker('uri')
    type = 'individual'


class BusinessSellerFactory(SellerFactory):
    class Meta:
        model = BusinessSeller

    type = 'business'
    ein = LazyFunction(gen.cnpj)
    business_name = Faker('company')
    business_phone = Faker('phone_number')
    business_email = Faker('safe_email')
    business_website = Faker('uri')
    business_opening_date = Faker('date_this_month')
    business_address = SubFactory(AddressModelFactory)
    owner = SubFactory(OwnerModelFactory)

    business_description = Faker('sentence', nb_words=5)
    business_facebook = Faker('uri')
    business_twitter = Faker('uri')
