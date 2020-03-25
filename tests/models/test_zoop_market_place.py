from unittest import TestCase

from ZoopAPIWrapper.models.base import ZoopMarketPlaceModel


class ZoopMarketPlaceModelTestCase(TestCase):
    @property
    def data(self):
        return {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            'marketplace_id': 'foo'
        }

    def test_from_dict(self):
        instance = ZoopMarketPlaceModel.from_dict(self.data)

        self.assertIsInstance(instance, ZoopMarketPlaceModel)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.marketplace_id, 'foo')

    def test_to_dict(self):
        instance = ZoopMarketPlaceModel.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
