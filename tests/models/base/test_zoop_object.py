from unittest.mock import patch, MagicMock

from tests.utils import SetTestCase
from ZoopAPIWrapper.exceptions import ValidationError
from tests.factories.base import ZoopObjectFactory
from ZoopAPIWrapper.models.base import ZoopObject


class ZoopObjectTestCase(SetTestCase):
    def setUp(self) -> None:
        self.patcher_fields = patch(
            'ZoopAPIWrapper.models.base.ZoopObject.get_fields')
        self.patcher_required_fields = patch(
            'ZoopAPIWrapper.models.base.ZoopObject.get_required_fields')
        self.patcher_non_required_fields = patch(
            'ZoopAPIWrapper.models.base.ZoopObject.get_non_required_fields')

        self.mocked_fields = self.patcher_fields.start()
        self.mocked_required_fields = self.patcher_required_fields.start()
        self.mocked_non_required_fields = self.patcher_non_required_fields\
            .start()

        self.addCleanup(self.patcher_fields.stop)
        self.addCleanup(self.patcher_required_fields.stop)
        self.addCleanup(self.patcher_non_required_fields.stop)

        self.mocked_fields.return_value = {'id', 'name'}
        self.mocked_required_fields.return_value = {'id'}
        self.mocked_non_required_fields.return_value = {'name'}

    @property
    def data(self):
        return {
            'id': 1,
            'name': None
        }

    def test_init(self):
        validate = MagicMock()
        instance = MagicMock(
            get_all_fields=MagicMock(return_value={'id', 'name'}),
            validate_fields=validate,
        )
        setattr(instance, 'id', None)
        setattr(instance, 'name', None)

        # noinspection PyCallByClass
        ZoopObject.__init__(instance, **self.data)

        self.assertEqual(instance.id, 1)
        self.assertIsNone(instance.name, 1)
        validate.assert_called_once()

    @patch('ZoopAPIWrapper.models.base.ZoopObject.validate_fields')
    def test_init_call_validate(self, mocked_validate):
        ZoopObjectFactory(id=1)
        mocked_validate.assert_called_once()

    @patch('ZoopAPIWrapper.models.base.ZoopObject.init_custom_fields')
    def test_init_call_init_custom_values(self, mocked_init_custom_fields):
        ZoopObjectFactory(id=1)
        mocked_init_custom_fields.assert_called_once()

    def test_create(self):
        instance = ZoopObjectFactory(id=1)
        self.assertIsInstance(instance, ZoopObject)

    def test_create_allow_empty(self):
        instance = ZoopObjectFactory(allow_empty=True)
        self.assertIsInstance(instance, ZoopObject)

    def test_create_dont_allow_empty(self):
        self.assertRaises(ValidationError, ZoopObjectFactory)

    def test_make_data_copy_with_args(self):
        data = {}
        new_data = ZoopObject.make_data_copy_with_kwargs(data, foo='bar')

        self.assertEqual(data, {})
        self.assertEqual(new_data.get('foo'), 'bar')

    def test_make_data_none_copy_with_args(self):
        data = None
        new_data = ZoopObject.make_data_copy_with_kwargs(data, foo='bar')

        self.assertEqual(data, None)
        self.assertEqual(new_data.get('foo'), 'bar')

    def test_from_dict_empty(self):
        data = {}
        self.assertRaises(ValidationError, ZoopObject.from_dict, data)

    def test_from_dict_allow_empty(self):
        data = {}
        instance = ZoopObject.from_dict(data, allow_empty=True)

        self.assertIsInstance(instance, ZoopObject)

    def test_from_dict(self):
        instance = ZoopObject.from_dict(self.data)

        self.assertIsInstance(instance, ZoopObject)
        self.assertEqual(instance.id, 1)
        self.assertIsNone(instance.name)

    def test_validate_allow_empty(self):
        instance = ZoopObjectFactory(allow_empty=True)
        self.assertIsInstance(instance, ZoopObject)

        instance.validate_fields()

    def test_validate_raise(self):
        instance = ZoopObjectFactory(id=1)
        self.assertIsInstance(instance, ZoopObject)

        instance.id = None

        self.assertRaises(ValidationError, instance.validate_fields)

    def test_validate_raise_false(self):
        instance = ZoopObjectFactory(id=1)
        self.assertIsInstance(instance, ZoopObject)

        instance.id = None

        instance.validate_fields(raise_exception=False)

    def test_is_value_empty(self):
        self.assertTrue(ZoopObject.is_value_empty(None))
        self.assertTrue(ZoopObject.is_value_empty({}))
        self.assertTrue(ZoopObject.is_value_empty([{}]))

        self.assertFalse(ZoopObject.is_value_empty([]))
        self.assertFalse(ZoopObject.is_value_empty(False))
        self.assertFalse(ZoopObject.is_value_empty(0))
        self.assertFalse(ZoopObject.is_value_empty(''))

    def test_to_dict(self):
        data = self.data
        data['foo'] = {}
        data['bar'] = [{}]
        data['foo2'] = MagicMock(
            to_dict=MagicMock(
                return_value={'foo2': 'foo2'}
            )
        )
        data['bar2'] = [MagicMock(
            to_dict=MagicMock(
                return_value={'bar2': 'bar2'}
            )
        )]

        self.mocked_fields.return_value = {
            'id', 'name', 'foo', 'bar', 'foo2', 'bar2'}

        instance = ZoopObject.from_dict(data)
        """We remove the name, foo and bar because it's values are 'empty'.
        So it won't return on to_dict method"""
        data.pop('name')
        data.pop('foo')
        data.pop('bar')

        """We need to transform the data to have equality"""
        data['foo2'] = data['foo2'].to_dict()
        data['bar2'][0] = data['bar2'][0].to_dict()

        self.assertIsInstance(instance, ZoopObject)
        self.assertEqual(instance.to_dict(), data)

    @staticmethod
    def test_get_all_fields():
        mocked_get_fields = MagicMock()
        instance = MagicMock(
            _allow_empty=False,
            get_fields=mocked_get_fields
        )

        ZoopObject.get_all_fields(instance)
        mocked_get_fields.assert_called_once()

    @staticmethod
    def test_get_validation_fields():
        mocked_required_fields = MagicMock()
        instance = MagicMock(
            _allow_empty=False,
            get_required_fields=mocked_required_fields
        )

        ZoopObject.get_validation_fields(instance)
        mocked_required_fields.assert_called_once()

    def test_fields(self):
        self.assertEqual(
            {"id", 'name'},
            ZoopObject.get_fields()
        )

    def test_required_fields(self):
        self.assertEqual(
            {'id'},
            ZoopObject.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertEqual(
            {'name'},
            ZoopObject.get_non_required_fields()
        )
