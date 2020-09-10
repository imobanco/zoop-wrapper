from unittest.mock import MagicMock, patch

from tests.utils import SetTestCase
from zoop_wrapper.models.invoice import Invoice, BillingInstructions
from tests.factories.invoice import BillingInstructionsFactory, InvoiceFactory


class InvoiceTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertIsSubSet(
            {"expiration_date", "payment_limit_date"}, Invoice.get_required_fields()
        )

    def test_non_required_fields(self):
        with patch(
            "zoop_wrapper.models.invoice.PaymentMethod.get_non_required_fields"
        ) as mocked_super_non_required_fields:
            mocked_super_non_required_fields.return_value = set()

            self.assertIsSubSet(
                {
                    "accepted",
                    "bank_code",
                    "barcode",
                    "billing_instructions",
                    "body_instructions",
                    "document_number",
                    "downloaded",
                    "fingerprint",
                    "paid_at",
                    "printed",
                    "recipient",
                    "reference_number",
                    "sequence",
                    "status",
                    "url",
                    "zoop_boleto_id",
                },
                Invoice.get_non_required_fields(),
            )

            mocked_super_non_required_fields.assert_called_once()

    def test_init_custom_fields_1(self):
        instance = MagicMock(spec=Invoice)

        billing_instructions = BillingInstructionsFactory().to_dict()

        Invoice.init_custom_fields(instance, billing_instructions=billing_instructions)

        self.assertIsInstance(instance.billing_instructions, BillingInstructions)

    def test_init_custom_fields_2(self):
        instance = InvoiceFactory(billing_instructions=None)

        instance.init_custom_fields()

        self.assertNotIn("billing_instructions", instance.to_dict())

    def test_create(self):
        instance = InvoiceFactory()
        self.assertIsInstance(instance, Invoice)
