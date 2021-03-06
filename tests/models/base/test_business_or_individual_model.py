from unittest.mock import MagicMock

from pycpfcnpj import gen

from tests.utils import SetTestCase
from zoop_wrapper.models.base import BusinessOrIndividualModel
from zoop_wrapper.exceptions import ValidationError


class BusinessOrIndividualTestCase(SetTestCase):
    def test_set_identifier_empty(self):
        instance = MagicMock()

        self.assertRaises(
            ValidationError,
            BusinessOrIndividualModel.set_identifier,
            instance,
            None,
            None,
        )

    def test_set_identifier_both(self):
        instance = MagicMock()

        self.assertRaises(
            ValidationError,
            BusinessOrIndividualModel.set_identifier,
            instance,
            "foo",
            "foo",
        )

    def test_set_identifier_taxpayer_id(self):
        instance = MagicMock(INDIVIDUAL_IDENTIFIER="taxpayer_id")

        cpf = gen.cpf()
        BusinessOrIndividualModel.set_identifier(instance, taxpayer_id=cpf)
        self.assertEqual(instance.taxpayer_id, cpf)

    def test_set_identifier_invalid_taxpayer_id(self):
        instance = MagicMock(INDIVIDUAL_IDENTIFIER="taxpayer_id")

        self.assertRaises(
            ValidationError,
            BusinessOrIndividualModel.set_identifier,
            instance,
            taxpayer_id="foo",
        )

    def test_set_identifier_ein(self):
        instance = MagicMock(BUSINESS_IDENTIFIER="ein")

        cnpj = gen.cnpj()
        BusinessOrIndividualModel.set_identifier(instance, ein=cnpj)
        self.assertEqual(instance.ein, cnpj)

    def test_set_identifier_invalid_ein(self):
        instance = MagicMock(BUSINESS_IDENTIFIER="ein")

        self.assertRaises(
            ValidationError,
            BusinessOrIndividualModel.set_identifier,
            instance,
            ein="foo",
        )

    def test_get_type_empty_raise(self):
        instance = MagicMock(ein=None, taxpayer_id=None)

        self.assertRaises(ValidationError, BusinessOrIndividualModel.get_type, instance)

    def test_get_type_both_raise(self):
        instance = MagicMock(ein="foo", taxpayer_id="foo")

        self.assertRaises(ValidationError, BusinessOrIndividualModel.get_type, instance)

    def test_get_type_business(self):
        instance = MagicMock(
            ein=gen.cnpj(),
            taxpayer_id=None,
            BUSINESS_IDENTIFIER="ein",
            INDIVIDUAL_IDENTIFIER="taxpayer_id",
        )

        self.assertEqual(
            BusinessOrIndividualModel.get_type(instance),
            BusinessOrIndividualModel.BUSINESS_TYPE,
        )

    def test_get_type_individual(self):
        instance = MagicMock(
            ein=None,
            taxpayer_id=gen.cpf(),
            BUSINESS_IDENTIFIER="ein",
            INDIVIDUAL_IDENTIFIER="taxpayer_id",
        )

        self.assertEqual(
            BusinessOrIndividualModel.get_type(instance),
            BusinessOrIndividualModel.INDIVIDUAL_TYPE,
        )

    def test_get_type_uri_business(self):
        instance = MagicMock(ein="foo")

        self.assertEqual(
            BusinessOrIndividualModel.get_type_uri(instance),
            instance.URI.get(instance.BUSINESS_TYPE),
        )

    def test_get_type_uri_individual(self):
        instance = MagicMock(taxpayer_id="foo")

        self.assertEqual(
            BusinessOrIndividualModel.get_type_uri(instance),
            instance.URI.get(instance.INDIVIDUAL_TYPE),
        )

    def test_get_validation_fields_individual(self):
        instance = BusinessOrIndividualModel(taxpayer_id=gen.cpf())

        self.assertEqual({"taxpayer_id"}, instance.get_validation_fields())

    def test_get_validation_fields_business(self):
        instance = BusinessOrIndividualModel(ein=gen.cnpj())

        self.assertEqual({"ein"}, instance.get_validation_fields())

    def test_get_all_fields_individual(self):
        instance = BusinessOrIndividualModel(taxpayer_id=gen.cpf())

        self.assertIsSubSet({"taxpayer_id"}, instance.get_all_fields())

    def test_get_all_fields_business(self):
        instance = BusinessOrIndividualModel(ein=gen.cnpj())

        self.assertIsSubSet({"ein"}, instance.get_all_fields())

    def test_get_non_required_fields(self):
        self.assertIsSubSet(set(), BusinessOrIndividualModel.get_non_required_fields())

    def test_get_required_fields(self):
        self.assertEqual(set(), BusinessOrIndividualModel.get_required_fields())

    def test_get_business_non_required_fields(self):
        self.assertIsSubSet(
            set(), BusinessOrIndividualModel.get_business_non_required_fields()
        )

    def test_get_business_required_fields(self):
        self.assertEqual(
            {"ein"}, BusinessOrIndividualModel.get_business_required_fields()
        )

    def test_get_individual_non_required_fields(self):
        self.assertIsSubSet(
            set(), BusinessOrIndividualModel.get_individual_non_required_fields()
        )

    def test_get_individual_required_fields(self):
        self.assertEqual(
            {"taxpayer_id"}, BusinessOrIndividualModel.get_individual_required_fields()
        )
