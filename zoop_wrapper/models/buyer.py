from pycpfcnpj import cpfcnpj

from .base import (
    MarketPlaceModel,
    Person,
    SocialModel,
    FinancialModel,
)
from ..exceptions import FieldError


class Buyer(MarketPlaceModel, Person, SocialModel, FinancialModel):
    """
    Represent a buyer.
    https://docs.zoop.co/reference#comprador-1

    The :attr:`RESOURCE` is used to identify this Model.
    Used to check against :attr:`.resource`!

    Attributes:
        default_receipt_delivery_method: ?
    """

    RESOURCE = "buyer"

    def validate_custom_fields(self, **kwargs):
        """
        O :attr:`taxpayer_id` precisa ser um CPF ou CNPJ válido. Então verificamos isso.

        Args:
            **kwargs:
        """
        errors = []

        if self._allow_empty:
            return errors

        if not cpfcnpj.validate(self.taxpayer_id):
            errors.append(FieldError("taxpayer_id", "taxpayer_id inválido!"))
        return errors

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union({"default_receipt_delivery_method"})
