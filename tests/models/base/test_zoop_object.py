from unittest.mock import patch, MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.exceptions import ValidationError
from tests.factories.base import ZoopObjectFactory
from zoop_wrapper.models.base import ZoopObject


class ZoopObjectTestCase(SetTestCase):
    def setUp(self) -> None:
        self.patcher_all_fields = patch(
            "zoop_wrapper.models.base.ZoopObject.get_all_fields"
        )
        self.patcher_required_fields = patch(
            "zoop_wrapper.models.base.ZoopObject.get_required_fields"
        )
        self.patcher_non_required_fields = patch(
            "zoop_wrapper.models.base.ZoopObject.get_non_required_fields"
        )
        self.patcher_get_original_different_fields_mapping = patch(
            "zoop_wrapper.models.base.ZoopObject.get_original_different_fields_mapping"
        )

        self.mocked_fields = self.patcher_all_fields.start()
        self.mocked_required_fields = self.patcher_required_fields.start()
        self.mocked_non_required_fields = self.patcher_non_required_fields.start()
        self.mocked_get_original_different_fields_mapping = (
            self.patcher_get_original_different_fields_mapping.start()
        )

        self.addCleanup(self.patcher_all_fields.stop)
        self.addCleanup(self.patcher_required_fields.stop)
        self.addCleanup(self.patcher_non_required_fields.stop)
        self.addCleanup(self.patcher_get_original_different_fields_mapping.stop)

        self.mocked_fields.return_value = {"id", "name", "modificado"}
        self.mocked_required_fields.return_value = {"id"}
        self.mocked_non_required_fields.return_value = {"name", "modificado"}
        self.mocked_get_original_different_fields_mapping.return_value = {
            "modificado": "original"
        }

    @property
    def data(self):
        return {"id": 1, "name": None, "modificado": "teste"}

    def test_init(self):
        validate = MagicMock()
        instance = MagicMock(
            get_all_fields=MagicMock(return_value={"id", "name"}),
            validate_fields=validate,
        )
        setattr(instance, "id", None)
        setattr(instance, "name", None)

        # noinspection PyCallByClass
        ZoopObject.__init__(instance, **self.data)

        self.assertEqual(instance.id, 1)
        self.assertIsNone(instance.name, 1)
        validate.assert_called_once()

    @patch("zoop_wrapper.models.base.ZoopObject.validate_fields")
    def test_init_call_validate(self, mocked_validate):
        ZoopObjectFactory(id=1)
        mocked_validate.assert_called_once()

    @patch("zoop_wrapper.models.base.ZoopObject.init_custom_fields")
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
        new_data = ZoopObject.make_data_copy_with_kwargs(data, foo="bar")

        self.assertEqual(data, {})
        self.assertEqual(new_data.get("foo"), "bar")

    def test_from_dict_empty(self):
        data = {}
        self.assertRaises(ValidationError, ZoopObject.from_dict, data)

    def test_from_dict_none_allow_empty(self):
        data = None
        instance = ZoopObject.from_dict(data, allow_empty=True)
        self.assertIsInstance(instance, ZoopObject)

    def test_from_dict_allow_empty(self):
        data = {}
        instance = ZoopObject.from_dict(data, allow_empty=True)

        self.assertIsInstance(instance, ZoopObject)

    def test_from_dict(self):
        instance = ZoopObject.from_dict(self.data)

        self.assertIsInstance(instance, ZoopObject)
        self.assertEqual(instance.id, 1)
        self.assertIsNone(instance.name)

    def test_from_dict_data_raise_if_not_none_or_dict(self):

        self.mocked_required_fields.return_value = set()

        other_values = [
            "",
            1,
            [],
            set(),
            (),
            1.0,
            [""],
            [1],
            [[]],
            [{}],
            [set()],
            [()],
            [1.0],
        ]
        for value in other_values:
            with self.subTest(f"Valor:{value}"):
                self.assertRaises(ValidationError, ZoopObject.from_dict, value)

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

    def test_validate_call_validate_custom_fields(self):
        """
        Dado que existe um zoopObject z1
        Quando for chamado z1.validate_fields()
        Então z1.validate_custom_fields() deve ter sido chamado
        """
        z1: ZoopObject = ZoopObjectFactory(id=1)

        with patch(
            "zoop_wrapper.models.base.ZoopObject.validate_custom_fields"
        ) as mocked_validate:
            z1.validate_fields()

            self.assertIsInstance(mocked_validate, MagicMock)
            mocked_validate.assert_called_once_with()

    def test_validate_custom_fields(self):
        """
        Dado que existe um zoopObject z1
        Quando for chamado z1.custom_validate_fields()
        Então deve ser retornado uma lista vazia
        """
        z1: ZoopObject = ZoopObjectFactory(id=1)

        expected = []

        result = z1.validate_custom_fields()

        self.assertEqual(expected, result)

    def test_get_original_fields_mapping(self):
        instance: ZoopObject = ZoopObjectFactory(id=1)

        expected = {"modificado": "original"}

        result = instance.get_original_different_fields_mapping()

        self.assertEqual(expected, result)

    def test_is_value_empty(self):
        self.assertTrue(ZoopObject.is_value_empty(None))
        self.assertTrue(ZoopObject.is_value_empty({}))
        self.assertTrue(ZoopObject.is_value_empty([{}]))

        self.assertFalse(ZoopObject.is_value_empty([]))
        self.assertFalse(ZoopObject.is_value_empty(False))
        self.assertFalse(ZoopObject.is_value_empty(0))
        self.assertFalse(ZoopObject.is_value_empty(""))

    def test_to_dict(self):
        data = self.data
        data["foo"] = {}
        data["bar"] = [{}]
        data["foo2"] = MagicMock(to_dict=MagicMock(return_value={"foo2": "foo2"}))
        data["bar2"] = [MagicMock(to_dict=MagicMock(return_value={"bar2": "bar2"}))]

        self.mocked_fields.return_value = {
            "bar",
            "bar2",
            "foo",
            "foo2",
            "id",
            "modificado",
            "name",
        }

        instance = ZoopObject.from_dict(data)
        self.assertIsInstance(instance, ZoopObject)

        expected = data
        """We remove the name, foo and bar because it's values are 'empty'.
        So they won't return on to_dict method"""
        expected.pop("name")
        expected.pop("foo")
        expected.pop("bar")

        """We need to transform the data to have equality"""
        expected["foo2"] = data["foo2"].to_dict()
        expected["bar2"][0] = data["bar2"][0].to_dict()

        """Mapeamento custom do original"""
        original_mapping = instance.get_original_different_fields_mapping()
        for custom, original in original_mapping.items():
            expected[original] = expected.pop(custom)

        result = instance.to_dict()

        self.assertEqual(expected, result)

    def test_get_all_fields(self):
        instance = MagicMock()

        expected = {"id", "name", "modificado"}

        result = ZoopObject.get_all_fields(instance)
        self.assertEqual(result, expected)

    @staticmethod
    def test_get_validation_fields():
        mocked_required_fields = MagicMock()
        instance = MagicMock(
            _allow_empty=False, get_required_fields=mocked_required_fields
        )

        ZoopObject.get_validation_fields(instance)
        mocked_required_fields.assert_called_once()

    def test_get_required_fields(self):
        self.assertEqual({"id"}, ZoopObject.get_required_fields())

    def test_get_non_required_fields(self):
        self.assertEqual({"name", "modificado"}, ZoopObject.get_non_required_fields())
