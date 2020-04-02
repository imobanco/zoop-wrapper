from tests.utils import SetTestCase
from ZoopAPIWrapper.models.base import SocialModel
from ZoopAPIWrapper.models.factories.base import SocialModelFactory


class SocialTestCase(SetTestCase):
    @property
    def data(self):
        return {
            "facebook": 'foo',
            "twitter": 'foo'
        }

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

    def test_from_dict(self):
        instance = SocialModel.from_dict(self.data)

        self.assertIsInstance(instance, SocialModel)
        self.assertEqual(instance.facebook, 'foo')
        self.assertEqual(instance.twitter, 'foo')

    def test_to_dict(self):
        instance = SocialModel.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
