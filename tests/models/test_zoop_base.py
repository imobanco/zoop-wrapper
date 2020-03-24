from unittest import TestCase

from ZoopAPIWrapper.models.base import ZoopBase


class ZoopBaseTestCase(TestCase):
    def test_from_dict(self):
        data = {}
        instance = ZoopBase.from_dict(data)

        self.assertIsInstance(instance, ZoopBase)

    def test_to_dict(self):
        data = {}
        instance = ZoopBase.from_dict(data)

        self.assertIsInstance(instance, ZoopBase)
        self.assertEqual(instance.to_dict(), data)
