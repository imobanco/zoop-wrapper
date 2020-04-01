from tests.utils import MockedAddressLoggerTestCase as TestCase, SetTestCase
from ZoopAPIWrapper.models.seller import (
    Seller, Person, Address)
from ZoopAPIWrapper.models.factories.seller import (
    SellerFactory, IndividualSellerFactory, BusinessSellerFactory)


class SellerTestCase(TestCase, SetTestCase):
    def test_required_fields(self):
        self.assertIsSuperSet(
            set(),
            Seller.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {"type", "statement_descriptor", "mcc",
             "show_profile_online", "is_mobile",
             "decline_on_fail_security_code",
             "decline_on_fail_zipcode",
             "merchant_code", "terminal_code"},
            Seller.get_non_required_fields()
        )

    def test_individual_required_fields(self):
        self.assertIsSubSet(
            set(),
            Seller.get_individual_required_fields()
        )

    def test_individual_non_required_fields(self):
        self.assertIsSubSet(
            {'website'},
            Seller.get_individual_non_required_fields()
        )

    def test_business_required_fields(self):
        self.assertIsSuperSet(
            {'ein', 'business_name', 'business_phone',
             'business_email', 'business_website',
             'business_opening_date', 'owner', 'business_address'},
            Seller.get_business_required_fields()
        )

    def test_business_non_required_fields(self):
        self.assertIsSubSet(
            {'business_description', 'business_facebook',
             'business_twitter'},
            Seller.get_business_non_required_fields()
        )

    def test_get_all_fields_business(self):
        instance = BusinessSellerFactory()
        self.assertIsInstance(instance, Seller)

        self.assertIsSubSet(
            {'business_name', 'business_phone',
             'business_email', 'business_website',
             'business_opening_date', 'owner',
             'business_address', 'business_description',
             'business_facebook', 'business_twitter'},
            instance.get_all_fields()
        )

    def test_get_all_fields_individual(self):
        instance = IndividualSellerFactory()
        self.assertIsInstance(instance, Seller)

        self.assertIsSubSet(
            {'website'},
            instance.get_all_fields()
        )

    def test_get_validation_fields_individual(self):
        instance = IndividualSellerFactory()
        self.assertIsInstance(instance, Seller)

        self.assertIsSubSet(
            set(),
            instance.get_validation_fields()
        )

    def test_business_get_validation_fields(self):
        instance = BusinessSellerFactory()
        self.assertIsInstance(instance, Seller)

        self.assertIsSubSet(
            {'business_name', 'business_phone',
             'business_email', 'business_website',
             'business_opening_date', 'owner', 'business_address'},
            instance.get_validation_fields()
        )

    def test_create(self):
        self.assertRaises(TypeError, SellerFactory)

    def test_create_individual(self):
        instance = IndividualSellerFactory()

        self.assertIsInstance(instance, Seller)

    def test_create_business(self):
        instance = BusinessSellerFactory()

        self.assertIsInstance(instance, Seller)
