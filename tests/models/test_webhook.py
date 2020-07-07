from unittest.mock import patch, MagicMock

from ..utils import SetTestCase
from zoop_wrapper.models.webhook import Webhook
from zoop_wrapper.exceptions import FieldError


class WebhookTestCase(SetTestCase):
    def test_get_required_fields(self):
        expected = {"method", "url", "event"}

        with patch('zoop_wrapper.models.webhook.super') as mocked_super:
            self.assertIsInstance(mocked_super, MagicMock)
            super_required_fields = mocked_super.return_value.get_required_fields
            super_required_fields.return_value = set()

            result = Webhook.get_required_fields()

            super_required_fields.assert_called_once_with()

        self.assertEqual(expected, result)

    def test_get_non_required_fields(self):
        expected = {"description"}

        with patch('zoop_wrapper.models.webhook.super') as mocked_super:
            self.assertIsInstance(mocked_super, MagicMock)
            super_get_nrf = mocked_super.return_value.get_non_required_fields
            super_get_nrf.return_value = set()

            result = Webhook.get_non_required_fields()

            super_get_nrf.assert_called_once_with()

        self.assertEqual(expected, result)

    def test_init_custom_fields(self):
        """
        testa se o init_custom_fields tem comportamente correto
        """
        instance = MagicMock()

        self.assertIsInstance(instance.method, MagicMock)
        self.assertIsInstance(instance.event, MagicMock)

        Webhook.init_custom_fields(instance)

        self.assertEqual(instance.method, 'POST')
        self.assertEqual(instance.event, [])

    def test_init_custom_fields_event(self):
        """
        testa se o tratamento do event no init_custom_fields tem comportamente correto
        """

        instance = MagicMock()

        self.assertIsInstance(instance.event, MagicMock)

        Webhook.init_custom_fields(instance, event='asd')

        self.assertEqual(instance.event, ['asd'])

    def test_validate_custom_fields_events_empty(self):
        """
        cenário onde a lista de eventos vem vazia
        """
        instance = Webhook(allow_empty=True)

        errors = instance.validate_custom_fields()

        self.assertEqual(len(errors), 1)
        error: FieldError = errors[0]
        self.assertEqual(error.name, 'event')
        self.assertIn('não pode ser vazia', error.reason)

    def test_validate_custom_fields_events_invalid(self):
        """
        cenário onde a lista de eventos é inválida
        """
        instance = Webhook(allow_empty=True, event=['asd'])

        errors = instance.validate_custom_fields()

        self.assertEqual(len(errors), 1)
        error: FieldError = errors[0]
        self.assertEqual(error.name, 'event')
        self.assertIn('não são válidos', error.reason)
