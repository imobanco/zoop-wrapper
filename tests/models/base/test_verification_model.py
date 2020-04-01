from tests.utils import SetTestCase
from ZoopAPIWrapper.models.base import VerificationModel
from ZoopAPIWrapper.models.factories.base import (
    VerificationModelFactory)


class VerificationModelTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertIsSuperSet(
            {'postal_code_check', 'address_line1_check'},
            VerificationModel.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertIsSuperSet(
            set(),
            VerificationModel.get_non_required_fields()
        )

    def test_create(self):
        instance = VerificationModelFactory()
        self.assertIsInstance(instance, VerificationModel)
