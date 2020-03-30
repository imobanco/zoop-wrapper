from unittest import TestCase

from ZoopAPIWrapper.models.base import VerificationModel
from ZoopAPIWrapper.models.factories.base import (
    VerificationModelFactory)


class VerificationModelTestCase(TestCase):
    @property
    def data(self):
        return {
            "postal_code_check": 'foo',
            "address_line1_check": 'foo'
        }

    def test_required_fields(self):
        fields = {'postal_code_check', 'address_line1_check'}
        self.assertTrue(
            fields.issuperset(VerificationModel.get_required_fields())
        )

    def test_non_required_fields(self):
        fields = set()
        self.assertTrue(
            fields.issuperset(VerificationModel.get_non_required_fields())
        )

    def test_create(self):
        instance = VerificationModelFactory()
        self.assertIsInstance(instance, VerificationModel)

    def test_from_dict(self):
        instance = VerificationModel.from_dict(self.data)

        self.assertIsInstance(instance, VerificationModel)
        self.assertEqual(instance.postal_code_check, 'foo')
        self.assertEqual(instance.address_line1_check, 'foo')

    def test_to_dict(self):
        instance = VerificationModel.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)