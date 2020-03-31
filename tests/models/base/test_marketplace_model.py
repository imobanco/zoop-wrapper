from tests.utils import SetTestCase
from ZoopAPIWrapper.models.base import MarketPlaceModel
from ZoopAPIWrapper.models.factories.base import MarketPlaceModelFactory


class MarketPlaceModelTestCase(SetTestCase):
    @property
    def data(self):
        return {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'created_at': 'foo',
            'updated_at': 'foo',

            'marketplace_id': 'foo'
        }

    def test_required_fields(self):
        self.assertIsSuperSet(
            set(),
            MarketPlaceModel.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {'marketplace_id'},
            MarketPlaceModel.get_non_required_fields()
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
