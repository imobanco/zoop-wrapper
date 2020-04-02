from tests.utils import SetTestCase
from ZoopAPIWrapper.models.base import MarketPlaceModel
from tests.factories.base import MarketPlaceModelFactory


class MarketPlaceModelTestCase(SetTestCase):
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
