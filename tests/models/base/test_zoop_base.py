from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from ZoopAPIWrapper.exceptions import ValidationError
from ZoopAPIWrapper.models.factories.base import ZoopBaseFactory
from ZoopAPIWrapper.models.base import ZoopBase


class ZoopBaseTestCase(TestCase):
    def setUp(self) -> None:
        self.patcher_fields = patch(
            'ZoopAPIWrapper.models.base.ZoopBase.fields',
            new_callable=PropertyMock)
        self.patcher_required_fields = patch(
            'ZoopAPIWrapper.models.base.ZoopBase.required_fields',
            new_callable=PropertyMock)
        self.patcher_non_required_fields = patch(
            'ZoopAPIWrapper.models.base.ZoopBase.non_required_fields',
            new_callable=PropertyMock)

        self.mocked_fields = self.patcher_fields.start()
        self.mocked_required_fields = self.patcher_required_fields.start()
        self.mocked_non_required_fields = self.patcher_non_required_fields.start()

        self.addCleanup(self.patcher_fields.stop)
        self.addCleanup(self.patcher_required_fields.stop)
        self.addCleanup(self.patcher_non_required_fields.stop)

        self.mocked_fields.return_value = ['id', 'name']
        self.mocked_required_fields.return_value = ['id']
        self.mocked_non_required_fields.return_value = ['name']

    @property
    def data(self):
        return {
            'id': 1,
            'name': None
        }

    def test_init(self):
        validate = MagicMock()
        instance = MagicMock(
            fields=['id', 'name'],
            required_fields=['id'],
            non_required_fields=['name'],
            validate_required_fields=validate
        )

        # noinspection PyCallByClass
        ZoopBase.__init__(instance, **self.data)

        self.assertEqual(instance.id, 1)
        self.assertIsNone(instance.name, 1)
        validate.assert_called_once()

    @patch('ZoopAPIWrapper.models.base.ZoopBase.validate_required_fields')
    def test_init_call_validate(self, mocked_validate):
        ZoopBaseFactory(id=1)
        mocked_validate.assert_called_once()

    def test_create(self):
        instance = ZoopBaseFactory(id=1)
        self.assertIsInstance(instance, ZoopBase)

    def test_create_allow_empty(self):
        instance = ZoopBaseFactory(allow_empty=True)
        self.assertIsInstance(instance, ZoopBase)

    def test_create_dont_allow_empty(self):
        self.assertRaises(ValidationError, ZoopBaseFactory)

    def test_validate(self):
        instance = ZoopBaseFactory(allow_empty=True)
        self.assertIsInstance(instance, ZoopBase)

        instance.validate_required_fields()

    def test_validate_raise(self):
        instance = ZoopBaseFactory(id=1)
        self.assertIsInstance(instance, ZoopBase)

        instance.id = None

        self.assertRaises(ValidationError, instance.validate_required_fields)

    def test_from_dict_empty(self):
        data = {}
        self.assertRaises(ValidationError, ZoopBase.from_dict, data)

    def test_from_dict_allow_empty(self):
        data = {}
        instance = ZoopBase.from_dict(data, allow_empty=True)

        self.assertIsInstance(instance, ZoopBase)

    def test_from_dict(self):
        instance = ZoopBase.from_dict(self.data)

        self.assertIsInstance(instance, ZoopBase)

    def test_to_dict(self):
        data = self.data

        instance = ZoopBase.from_dict(data)

        """We remove the name because it's value is none.
        So it won't return on to_dict method"""
        data.pop('name')

        self.assertIsInstance(instance, ZoopBase)
        self.assertEqual(instance.to_dict(), data)

    def test_to_dict_allow_empty(self):
        instance = ZoopBase.from_dict(self.data, allow_empty=True)

        self.assertIsInstance(instance, ZoopBase)
        self.assertEqual(instance.to_dict(), self.data)
