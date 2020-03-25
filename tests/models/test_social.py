from unittest import TestCase

from ZoopAPIWrapper.models.seller import SocialModel


class SocialTestCase(TestCase):
    @property
    def data(self):
        return {
            "facebook": 'foo',
            "twitter": 'foo'
        }

    def test_from_dict(self):
        instance = SocialModel.from_dict(self.data)

        self.assertIsInstance(instance, SocialModel)
        self.assertEqual(instance.facebook, 'foo')
        self.assertEqual(instance.twitter, 'foo')

    def test_to_dict(self):
        instance = SocialModel.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)