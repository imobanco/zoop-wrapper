from unittest.mock import patch, MagicMock

from ..utils import SetTestCase
from ..factories.webhook import WebhookFactory
from zoop_wrapper.models.webhook import Webhook
from zoop_wrapper.exceptions import FieldError


class WebhookTestCase(SetTestCase):
    def test_get_required_fields(self):
        """
        Testa se o conjunto de campos obrigatrórios está correto

        Dado N/A
        Quando for chamado Webhook.get_required_fields()
        Então:
            - o super().get_required_fields() deve ter sido chamado
            - o resultado deve ser igual à {"method", "url", "events"}
        """
        expected = {"method", "url", "events"}

        with patch("zoop_wrapper.models.webhook.super") as mocked_super:
            self.assertIsInstance(mocked_super, MagicMock)
            super_required_fields = mocked_super.return_value.get_required_fields
            super_required_fields.return_value = set()

            result = Webhook.get_required_fields()

            super_required_fields.assert_called_once_with()

        self.assertEqual(expected, result)

    def test_get_non_required_fields(self):
        """
        Testa se o conjunto de campos opcionais está correto

        Dado N/A
        Quando for chamado Webhook.get_non_required_fields()
        Então:
            - o super().get_non_required_fields() deve ter sido chamado
            - o resultado deve ser igual à {"description", "authorization", "dflag", "status", "events_sent"}
        """
        expected = {"description", "authorization", "dflag", "status", "events_sent"}

        with patch("zoop_wrapper.models.webhook.super") as mocked_super:
            self.assertIsInstance(mocked_super, MagicMock)
            super_get_nrf = mocked_super.return_value.get_non_required_fields
            super_get_nrf.return_value = set()

            result = Webhook.get_non_required_fields()

            super_get_nrf.assert_called_once_with()

        self.assertEqual(expected, result)

    def test_get_original_differente_fields_mapping(self):
        """
        Testa se o dicionário de mapeamento de campos custom => original está correto

        Dado N/A
        Quando for chamado Webhook.get_original_different_fields_mapping()
        Então o resultado deve ser igual à {"events": "event"}
        """

        instance: Webhook = WebhookFactory()

        expected = {"events": "event"}

        result = instance.get_original_different_fields_mapping()

        self.assertEqual(expected, result)

    def test_init_custom_fields(self):
        """
        Testa se o init_custom_fields declarou os campos `method` e `events` corretamente

        Dado que exista um Webhook w1
        Quando for chamado w1.init_custom_fields()
        Então:
            w1.method deve ser igual à "POST"
            w1.events deve ser igual à []
        """
        w1: Webhook = MagicMock()

        self.assertIsInstance(w1.method, MagicMock)
        self.assertIsInstance(w1.events, MagicMock)

        Webhook.init_custom_fields(w1)

        self.assertEqual(w1.method, "POST")
        self.assertEqual(w1.events, [])

    def test_init_custom_fields_event(self):
        """
        testa se o tratamento do events no init_custom_fields fez o parse para lista corretamente

        Dado que exista um Webhook w1
        Quando for chamado w1.init_custom_fields(events="asd")
        Então w1.events deve ser igual à ["asd"]
        """

        w1: Webhook = MagicMock()

        self.assertIsInstance(w1.events, MagicMock)

        Webhook.init_custom_fields(w1, events="asd")

        self.assertEqual(w1.events, ["asd"])

    def test_validate_custom_fields_events_empty(self):
        """
        cenário onde a lista de eventos vem vazia
        """
        instance = WebhookFactory(events=[], allow_empty=True)

        errors = instance.validate_custom_fields()

        self.assertEqual(len(errors), 1)
        error: FieldError = errors[0]
        self.assertEqual(error.name, "events")
        self.assertIn("não pode ser vazia", error.reason)

    def test_validate_custom_fields_events_invalid(self):
        """
        cenário onde a lista de eventos é inválida
        """
        instance = WebhookFactory(events=["asd"], allow_empty=True)

        errors = instance.validate_custom_fields()

        self.assertEqual(len(errors), 1)
        error: FieldError = errors[0]
        self.assertEqual(error.name, "events")
        self.assertIn("não são válidos", error.reason)
