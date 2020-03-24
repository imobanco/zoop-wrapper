from unittest import TestCase

from ZoopAPIWrapper.models.base import ZoopBase


class ZoopBaseTestCase(TestCase):
    def setUp(self) -> None:
        ZoopBase._ZoopBase__FIELDS = ['id', 'name']

    def tearDown(self) -> None:
        ZoopBase._ZoopBase__FIELDS = []

    def test_from_dict(self):
        data = {}
        instance = ZoopBase.from_dict(data)

        self.assertIsInstance(instance, ZoopBase)

    def test_to_dict(self):
        data = {
            "id": '1',
            "name": None
        }
        instance = ZoopBase.from_dict(data)

        instance.id = '1'
        instance.name = None

        data.pop('name')

        self.assertIsInstance(instance, ZoopBase)
        self.assertEqual(instance.to_dict(), data)
