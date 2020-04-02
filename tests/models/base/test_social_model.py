from tests.utils import SetTestCase
from ZoopAPIWrapper.models.base import SocialModel
from tests.factories.base import SocialModelFactory


class SocialTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertIsSuperSet(
            set(),
            SocialModel.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertIsSuperSet(
            {'facebook', 'twitter'},
            SocialModel.get_non_required_fields()
        )

    def test_create(self):
        instance = SocialModelFactory()
        self.assertIsInstance(instance, SocialModel)
