from tests.utils import SetTestCase
from tests.factories.base import ResourceModelFactory
from ZoopAPIWrapper.models.base import ResourceModel


class ResourceModelTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertEqual(
            set(),
            ResourceModel.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertEqual(
            {"id", "resource", "uri", "created_at",
             "updated_at", "metadata"},
            ResourceModel.get_non_required_fields()
        )

    def test_create(self):
        instance = ResourceModelFactory()
        self.assertIsInstance(instance, ResourceModel)
