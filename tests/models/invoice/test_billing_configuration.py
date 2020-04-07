from unittest.mock import patch, MagicMock

from tests.utils import SetTestCase
from ZoopAPIWrapper.exceptions import ValidationError
from ZoopAPIWrapper.models.invoice import BillingConfiguration
from tests.factories.invoice import (
    BillingConfigurationFactory, FixedDiscountFactory,
    PercentDiscountFactory, FixedFeeFactory, PercentFeeFactory
)
from ZoopAPIWrapper.exceptions import ValidationError


class BillingConfigurationTestCase(SetTestCase):
    def test_create_set_type_fail(self):
        self.assertRaises(
            ValidationError,
            BillingConfigurationFactory
        )

    def test_create_validation_fail(self):
        self.assertRaises(
            ValidationError,
            BillingConfigurationFactory,
            mode=BillingConfiguration.FIXED_MODE,
            is_discount=False
        )

    def test_create_empty(self):
        instance = BillingConfigurationFactory(
            mode=BillingConfiguration.FIXED_MODE,
            is_discount=False,
            allow_empty=True
        )
        self.assertIsInstance(instance, BillingConfiguration)

    @patch('ZoopAPIWrapper.models.invoice.BillingConfiguration.set_type')
    def test_init_custom_fields(self, mocked_set_type):
        instance = MagicMock(
            _allow_empty=False,
            set_type=mocked_set_type
        )

        BillingConfiguration.init_custom_fields(instance, 'foo', 'foo')

        self.assertIsInstance(mocked_set_type, MagicMock)
        mocked_set_type.assert_called_once_with('foo', 'foo')

    @staticmethod
    def test_validate_mode():
        instance = MagicMock(
            _allow_empty=False,
            mode='foo'
        )
        BillingConfiguration.validate_mode(instance, BillingConfiguration.FIXED_MODE)

    def test_validate_mode_raise(self):
        instance = MagicMock(
            _allow_empty=False,
            mode='foo'
        )
        self.assertRaises(
            ValidationError,
            BillingConfiguration.validate_mode,
            instance,
            'foo'
        )

    def test_set_type(self):
        instance = MagicMock(
            MODES=BillingConfiguration.MODES
        )

        BillingConfiguration.set_type(
            instance, BillingConfiguration.FIXED_MODE, True)
        self.assertEqual(instance.mode, BillingConfiguration.FIXED_MODE)
        self.assertEqual(instance.is_discount, True)

    def test_required_fields(self):
        self.assertEqual(
            {'mode'},
            BillingConfiguration.get_required_fields()
        )

    def test_get_fee_required_fields(self):
        self.assertIsSubSet(
            {'start_date'},
            BillingConfiguration.get_fee_required_fields()
        )

    def test_get_discount_required_fields(self):
        self.assertIsSubSet(
            {'limit_date'},
            BillingConfiguration.get_discount_required_fields()
        )

    def test_get_fixed_required_fields(self):
        self.assertIsSubSet(
            {'amount'},
            BillingConfiguration.get_fixed_required_fields()
        )

    def test_get_percent_required_fields(self):
        self.assertIsSubSet(
            {'percentage'},
            BillingConfiguration.get_percent_required_fields()
        )

    def test_get_all_fields(self):
        instance = MagicMock(
            get_validation_fields=MagicMock(
                return_value=set()
            )
        )

        self.assertEqual(
            set(),
            BillingConfiguration.get_all_fields(instance)
        )

    def test_get_validation_fields_allow_empty(self):
        instance = BillingConfiguration(allow_empty=True)
        self.assertIsInstance(instance, BillingConfiguration)

        self.assertEqual(
            {'mode'},
            instance.get_validation_fields()
        )

    def test_get_validation_fields_fixed_discount(self):
        instance = FixedDiscountFactory(allow_empty=True)
        self.assertIsInstance(instance, BillingConfiguration)

        self.assertEqual(
            {'mode', 'limit_date', 'amount'},
            instance.get_validation_fields()
        )

    def test_get_validation_fields_percent_discount(self):
        instance = PercentDiscountFactory(allow_empty=True)
        self.assertIsInstance(instance, BillingConfiguration)

        self.assertEqual(
            {'mode', 'limit_date', 'percentage'},
            instance.get_validation_fields()
        )

    def test_get_validation_fields_fixed_fee(self):
        instance = FixedFeeFactory(allow_empty=True)
        self.assertIsInstance(instance, BillingConfiguration)

        self.assertEqual(
            {'mode', 'start_date', 'amount'},
            instance.get_validation_fields()
        )

    def test_get_validation_fields_percent_fee(self):
        instance = PercentFeeFactory(allow_empty=True)
        self.assertIsInstance(instance, BillingConfiguration)

        self.assertEqual(
            {'mode', 'start_date', 'percentage'},
            instance.get_validation_fields()
        )
