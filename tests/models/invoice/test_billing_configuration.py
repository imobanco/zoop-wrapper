from unittest.mock import patch, MagicMock

from tests.utils import SetTestCase
from ZoopAPIWrapper.exceptions import ValidationError
from ZoopAPIWrapper.models.invoice import BillingConfiguration
from ZoopAPIWrapper.models.factories.invoice import (
    BillingConfigurationFactory, FixedDiscountFactory,
    PercentDiscountFactory, FixedFeeFactory, PercentFeeFactory
)


class BillingConfigurationTestCase(SetTestCase):
    @property
    def data(self):
        return {
            "mode": BillingConfiguration.FIXED_MODE,
            "amount": 'foo',
            "start_date": 'foo'
        }

    def test_create_config_mode_fail(self):
        self.assertRaises(
            TypeError,
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

    @patch('ZoopAPIWrapper.models.invoice.BillingConfiguration.config_mode')
    def test_init_custom_fields(self, mocked_config_mode):
        instance = MagicMock(
            config_mode=mocked_config_mode
        )

        BillingConfiguration.init_custom_fields(instance, 'foo', 'foo')

        self.assertIsInstance(mocked_config_mode, MagicMock)
        mocked_config_mode.assert_called_once_with('foo', 'foo')

    def test_config_mode(self):
        instance = MagicMock(
            MODES=BillingConfiguration.MODES
        )

        BillingConfiguration.config_mode(instance, BillingConfiguration.FIXED_MODE, True)
        self.assertEqual(instance.mode, BillingConfiguration.FIXED_MODE)
        self.assertEqual(instance.is_discount, True)

    def test_config_mode_raise(self):
        instance = MagicMock(
            MODES=BillingConfiguration.MODES
        )

        self.assertRaises(
            TypeError,
            BillingConfiguration.config_mode,
            instance, 'foo', True
        )

    def test_required_fields(self):
        self.assertIsSuperSet(
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

        self.assertIsSuperSet(
            set(),
            BillingConfiguration.get_all_fields(instance)
        )

    def test_get_validation_fields_fixed_discount(self):
        instance = FixedDiscountFactory()
        self.assertIsInstance(instance, BillingConfiguration)

        self.assertIsSuperSet(
            {'mode', 'limit_date', 'amount'},
            instance.get_validation_fields()
        )

    def test_get_validation_fields_percent_discount(self):
        instance = PercentDiscountFactory()
        self.assertIsInstance(instance, BillingConfiguration)

        self.assertIsSuperSet(
            {'mode', 'limit_date', 'percentage'},
            instance.get_validation_fields()
        )

    def test_get_validation_fields_fixed_fee(self):
        instance = FixedFeeFactory()
        self.assertIsInstance(instance, BillingConfiguration)

        self.assertIsSuperSet(
            {'mode', 'start_date', 'amount'},
            instance.get_validation_fields()
        )

    def test_get_validation_fields_percent_fee(self):
        instance = PercentFeeFactory()
        self.assertIsInstance(instance, BillingConfiguration)

        self.assertIsSuperSet(
            {'mode', 'start_date', 'percentage'},
            instance.get_validation_fields()
        )

    def test_from_dict(self):
        instance = BillingConfiguration.from_dict(self.data)

        self.assertIsInstance(instance, BillingConfiguration)
        self.assertEqual(instance.mode, BillingConfiguration.FIXED_MODE)
        self.assertEqual(instance.amount, 'foo')
        self.assertEqual(instance.start_date, 'foo')

    def test_to_dict(self):
        instance = BillingConfiguration.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
