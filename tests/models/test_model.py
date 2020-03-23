from unittest import TestCase

from ZoopAPIWrapper.models import ZoopModel


class ZoopModelTestCase(TestCase):
    def test_from_dict(self):
        data = {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo'
        }
        instance = ZoopModel.from_dict(data)

        self.assertIsInstance(instance, ZoopModel)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.resource, 'foo')
        self.assertEqual(instance.uri, 'foo')
        self.assertEqual(instance.metadata, {})
        self.assertEqual(instance.created_at, 'foo')
        self.assertEqual(instance.updated_at, 'foo')

    def test_to_dict(self):
        data = {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo'
        }
        instance = ZoopModel.from_dict(data)

        self.assertIsInstance(instance, ZoopModel)
        self.assertEqual(instance.to_dict(), data)
