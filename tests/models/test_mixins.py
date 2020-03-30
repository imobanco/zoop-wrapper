from unittest import TestCase

from ZoopAPIWrapper.models.mixins import BusinessOrIndividualMixin


class BusinessOrIndividualTestCase(TestCase):
    def test_set_identifier_empty(self):
        instance = BusinessOrIndividualMixin()

        self.assertRaises(TypeError, instance.set_identifier, None, None)

    def test_set_identifier_both(self):
        instance = BusinessOrIndividualMixin()

        self.assertRaises(TypeError, instance.set_identifier, 'foo', 'foo')

    def test_set_identifier_taxpayer_id(self):
        instance = BusinessOrIndividualMixin()

        instance.set_identifier(taxpayer_id='foo')
        self.assertEqual(instance.taxpayer_id, 'foo')

    def test_set_identifier_ein(self):
        instance = BusinessOrIndividualMixin()

        instance.set_identifier(ein='foo')
        self.assertEqual(instance.ein, 'foo')

    def test_get_type_empty_raise(self):
        instance = BusinessOrIndividualMixin()

        self.assertRaises(TypeError, instance.get_type)

    def test_get_type_both_raise(self):
        instance = BusinessOrIndividualMixin()

        setattr(instance, instance.BUSINESS_IDENTIFIER, 'foo')
        setattr(instance, instance.INDIVIDUAL_IDENTIFIER, 'foo')

        self.assertRaises(TypeError, instance.get_type)

    def test_get_type_business(self):
        instance = BusinessOrIndividualMixin()

        setattr(instance, instance.BUSINESS_IDENTIFIER, 'foo')

        self.assertEqual(instance.get_type(), instance.BUSINESS_TYPE)

    def test_get_type_individual(self):
        instance = BusinessOrIndividualMixin()

        setattr(instance, instance.INDIVIDUAL_IDENTIFIER, 'foo')

        self.assertEqual(instance.get_type(), instance.INDIVIDUAL_TYPE)

    def test_get_type_uri_business(self):
        instance = BusinessOrIndividualMixin()

        setattr(instance, instance.BUSINESS_IDENTIFIER, 'foo')

        self.assertEqual(instance.get_type_uri(), instance.URI.get(instance.BUSINESS_TYPE))

    def test_get_type_uri_individual(self):
        instance = BusinessOrIndividualMixin()

        setattr(instance, instance.INDIVIDUAL_IDENTIFIER, 'foo')

        self.assertEqual(instance.get_type_uri(), instance.URI.get(instance.INDIVIDUAL_TYPE))
