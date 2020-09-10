from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.exceptions import ValidationError
from zoop_wrapper.models.invoice import BaseModeObject


class BaseModeObjectTestCase(SetTestCase):
    def test_modes(self):
        modes = set()

        self.assertSetEqual(BaseModeObject.MODES, modes)

    def test_required_fields(self):
        expected = {"mode"}

        result = BaseModeObject.get_required_fields()

        self.assertSetEqual(result, expected)

    def test_fixed_required_fields(self):
        expected = {"amount", "mode"}

        result = BaseModeObject.get_fixed_required_fields()

        self.assertSetEqual(result, expected)

    def test_percentage_required_fields(self):
        expected = {"percentage", "mode"}

        result = BaseModeObject.get_percentage_required_fields()

        self.assertSetEqual(result, expected)

    def test_init_custom_fields_1(self):
        """
        Dado que:
            - existe um objeto instance com mode=None e MODES={"foo"}
        Quando for chamado BaseModeObject.init_custom_fields(instance, mode='foo')
        Então instance.mode deve ser 'foo'
        """
        instance = MagicMock(mode=None, MODES={"foo"})

        self.assertEqual(instance.mode, None)

        BaseModeObject.init_custom_fields(instance, mode="foo")

        self.assertEqual(instance.mode, "foo")

    def test_init_custom_fields_2(self):
        """
        Dado que:
            - existe um objeto instance com mode=None
            - BaseModeObject.MODES={'foo'}
        Quando for chamado BaseModeObject.init_custom_fields(instance, mode='bar')
        Então instance.mode deve ser None
        """
        instance = MagicMock(mode=None, MODES={"foo"})

        self.assertEqual(instance.mode, None)

        with self.assertRaises(ValidationError):
            BaseModeObject.init_custom_fields(instance, mode="bar")

        self.assertEqual(instance.mode, None)

    def test_get_mode_required_fields_mapping(self):
        instance = MagicMock()

        with self.assertRaises(NotImplementedError):
            BaseModeObject.get_mode_required_fields_mapping(instance)

    def test_get_validation_fields(self):
        """
        Dado que:
            - existe um método mockado foo_type_required_fields
            - existe um método mockado get_mode_required_fields_mapping que retorna:
                - {"foo": foo_type_required_fields}
            - existe um objeto instance com:
                - mode='foo'
                - MODES={"foo"}
                - get_mode_required_fields_mapping=get_mode_required_fields_mapping
        Quando for chamado BaseModeObject.get_validation_fields(instance)
        Então:
            - foo_type_required_fields deve ter sido chamado uma vez
            - o resultado deve ser foo_type_required_fields.return_value
        """

        foo_type_required_fields = MagicMock()
        get_mode_required_fields_mapping = MagicMock(
            return_value={"foo": foo_type_required_fields}
        )

        instance = MagicMock(
            mode="foo",
            MODES={"foo"},
            get_mode_required_fields_mapping=get_mode_required_fields_mapping,
        )

        result = BaseModeObject.get_validation_fields(instance)

        foo_type_required_fields.assert_called_once()

        self.assertEqual(result, foo_type_required_fields.return_value)
