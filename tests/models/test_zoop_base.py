from unittest import TestCase

from ZoopAPIWrapper.models.base import ZoopBase


class ZoopBaseTestCase(TestCase):
    def setUp(self) -> None:
        """
        ZoopBase model doesn't have any attribute.
        So we can manipulate it's attributes to test to_dict method
        """
        ZoopBase._ZoopBase__FIELDS = ['id', 'name']

    def tearDown(self) -> None:
        ZoopBase._ZoopBase__FIELDS = []

    @property
    def data(self):
        return {}

    def test_from_dict(self):
        """
        ZoopBase model doesn't have any attribute.
        So we can create a instance with an empty dict
        """
        instance = ZoopBase.from_dict(self.data)

        self.assertIsInstance(instance, ZoopBase)

    def test_to_dict(self):
        """
        ZoopBase model doesn't have any attribute.
        So we can manipulate it's attributes to test to_dict method
        """
        data = self.data
        data["id"] = '1'
        data["name"] = None

        instance = ZoopBase.from_dict(data)

        instance.id = '1'
        instance.name = None

        """We remove the name because it's value is none.
        So it won't return on to_dict method"""
        data.pop('name')

        self.assertIsInstance(instance, ZoopBase)
        self.assertEqual(instance.to_dict(), data)
