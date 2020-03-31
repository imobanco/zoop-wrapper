from unittest.mock import patch, MagicMock

from tests.utils import SetTestCase
from ZoopAPIWrapper.exceptions import ValidationError
from ZoopAPIWrapper.models.factories.base import ZoopObjectFactory
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

    def test_create(self):
        instance = ZoopObjectFactory(id=1)
        self.assertIsInstance(instance, ZoopObject)

    def test_create_allow_empty(self):
        instance = ZoopObjectFactory(allow_empty=True)
        self.assertIsInstance(instance, ZoopObject)

    def test_create_dont_allow_empty(self):
        self.assertRaises(ValidationError, ZoopObjectFactory)

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

    def test_to_dict(self):
        data = self.data

        instance = ZoopObject.from_dict(data)

        """We remove the name because it's value is none.
        So it won't return on to_dict method"""
        data.pop('name')

        self.assertIsInstance(instance, ZoopObject)
        self.assertEqual(instance.to_dict(), data)

    def test_get_all_fields(self):
        instance = ZoopObject(allow_empty=True)

        self.assertIsSuperSet(
            instance.get_all_fields(),
            ZoopObject.get_fields()
        )

    def test_get_validation_fields(self):
        instance = ZoopObject(allow_empty=True)

        self.assertIsSuperSet(
            instance.get_validation_fields(),
            ZoopObject.get_required_fields()
        )

    def test_fields(self):
        self.assertIsSuperSet(
            {"id", 'name'},
            ZoopObject.get_fields()
        )

    def test_required_fields(self):
        self.assertIsSuperSet(
            {'id'},
            ZoopObject.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertIsSuperSet(
            {'name'},
            ZoopObject.get_non_required_fields()
        )
