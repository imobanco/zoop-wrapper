from tests.utils import SetTestCase
from ZoopAPIWrapper.models.factories.base import ResourceModelFactory
from ZoopAPIWrapper.models.base import ResourceModel


class ResourceModelTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertIsSuperSet(
            set(),
            ResourceModel.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertIsSuperSet(
            {"id", "resource", "uri", "created_at",
             "updated_at", "metadata"},
            ResourceModel.get_non_required_fields()
        )

    def test_create(self):
        instance = ResourceModelFactory()
        self.assertIsInstance(instance, ResourceModel)
