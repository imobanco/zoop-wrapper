from unittest import TestCase

from ZoopAPIWrapper.models.factories.base import ZoopModelFactory
from ZoopAPIWrapper.models.base import ZoopModel


class ZoopModelTestCase(TestCase):
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

    def test_create(self):
        instance = ZoopModelFactory()
        self.assertIsInstance(instance, ZoopModel)

    def test_from_dict(self):
        instance = ZoopModel.from_dict(self.data)

        self.assertIsInstance(instance, ZoopModel)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.resource, 'foo')
        self.assertEqual(instance.uri, 'foo')
        self.assertEqual(instance.metadata, {})
        self.assertEqual(instance.created_at, 'foo')
        self.assertEqual(instance.updated_at, 'foo')

    def test_to_dict(self):
        instance = ZoopModel.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
