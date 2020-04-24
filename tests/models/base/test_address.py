from tests.utils import SetTestCase
from zoop_wrapper.models.base import Address
from tests.factories.base import AddressFactory


class AddressTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertEqual(set(), Address.get_required_fields())

    def test_non_required_fields(self):
        self.assertEqual(
            {
                "line1",
                "line2",
                "line3",
                "neighborhood",
                "city",
                "state",
                "postal_code",
                "country_code",
            },
            Address.get_non_required_fields(),
        )

    def test_create(self):
        instance = AddressFactory()
        self.assertIsInstance(instance, Address)
