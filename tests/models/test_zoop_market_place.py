from unittest import TestCase

from ZoopAPIWrapper.models.base import ZoopMarketPlaceModel


class ZoopMarketPlaceModelTestCase(TestCase):
    def test_from_dict(self):
        data = {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            'marketplace_id': 'foo'
        }
        instance = ZoopMarketPlaceModel.from_dict(data)

        self.assertIsInstance(instance, ZoopMarketPlaceModel)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.marketplace_id, 'foo')

    def test_to_dict(self):
        data = {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            'marketplace_id': 'foo'
        }
        instance = ZoopMarketPlaceModel.from_dict(data)

        self.assertIsInstance(instance, ZoopMarketPlaceModel)
        self.assertEqual(instance.to_dict(), data)
