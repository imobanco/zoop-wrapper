from tests.utils import SetTestCase
from ZoopAPIWrapper.models.factories.base import ResourceModelFactory
from ZoopAPIWrapper.models.base import ResourceModel


class ResourceModelTestCase(SetTestCase):
    @property
    def data(self):
        return {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo'
        }

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

    def test_from_dict(self):
        instance = ResourceModel.from_dict(self.data)

        self.assertIsInstance(instance, ResourceModel)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.resource, 'foo')
        self.assertEqual(instance.uri, 'foo')
        self.assertEqual(instance.metadata, {})
        self.assertEqual(instance.created_at, 'foo')
        self.assertEqual(instance.updated_at, 'foo')

    def test_to_dict(self):
        data = self.data
        instance = ResourceModel.from_dict(data)

        data.pop('metadata')
        self.assertEqual(instance.to_dict(), data)
