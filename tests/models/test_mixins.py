from unittest import TestCase
from unittest.mock import patch, MagicMock

from ZoopAPIWrapper.models.mixins import BusinessOrIndividualMixin


class BusinessOrIndividualTestCase(TestCase):
    def test_extract_identifier_missing(self):
        data = {}

        self.assertRaises(
            TypeError,
            BusinessOrIndividualMixin.
                _BusinessOrIndividualMixin__extract_identifier,  # noqa
            data
        )

    def test_extract_identifier_both(self):
        data = {
            'taxpayer_id': 'foo',
            'ein': 'foo'
        }

        self.assertRaises(
            TypeError,
            BusinessOrIndividualMixin.
                _BusinessOrIndividualMixin__extract_identifier,  # noqa
            data
        )

    def test_extract_identifier_individual(self):
        data = {
            'taxpayer_id': 'foo'
        }

        indentifier_type = BusinessOrIndividualMixin\
            ._BusinessOrIndividualMixin__extract_identifier(data)
        self.assertEqual(indentifier_type, 'taxpayer_id')

    def test_extract_identifier_business(self):
        data = {
            'ein': 'foo'
        }

        indentifier_type = BusinessOrIndividualMixin\
            ._BusinessOrIndividualMixin__extract_identifier(data)
        self.assertEqual(indentifier_type, 'ein')

    @patch('ZoopAPIWrapper.models.mixins.BusinessOrIndividualMixin.individual_class')  # noqa
    def test_get_class_individual(self, mocked_class):
        self.assertIsInstance(mocked_class, MagicMock)

        data = {
            'taxpayer_id': 'foo'
        }

        klass = BusinessOrIndividualMixin.get_class(data)
        self.assertEqual(klass, mocked_class)

    @patch('ZoopAPIWrapper.models.mixins.BusinessOrIndividualMixin.business_class')  # noqa
    def test_get_class_business(self, mocked_class):
        self.assertIsInstance(mocked_class, MagicMock)

        data = {
            'ein': 'foo'
        }

        klass = BusinessOrIndividualMixin.get_class(data)
        self.assertEqual(klass, mocked_class)
