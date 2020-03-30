from unittest import TestCase

from ZoopAPIWrapper.models.base import MarketPlaceModel
from ZoopAPIWrapper.models.factories.base import MarketPlaceModelFactory


class MarketPlaceModelTestCase(TestCase):
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

    def test_required_fields(self):
        fields = set()
        self.assertTrue(
            fields.issuperset(MarketPlaceModel.get_required_fields())
        )

    def test_non_required_fields(self):
        fields = {'marketplace_id'}
        self.assertTrue(
            fields.issubset(MarketPlaceModel.get_non_required_fields())
        )

    def test_create(self):
        instance = MarketPlaceModelFactory()
        self.assertIsInstance(instance, MarketPlaceModel)

    def test_from_dict(self):
        instance = MarketPlaceModel.from_dict(self.data)

        self.assertIsInstance(instance, MarketPlaceModel)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.marketplace_id, 'foo')

    def test_to_dict(self):
        instance = MarketPlaceModel.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
