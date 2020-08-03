from card_identifier.cardutils import validate_card

from .base import ResourceModel, BusinessOrIndividualModel
from .bank_account import BankAccount
from .card import Card
from ..utils import get_logger
from ..exceptions import FieldError, ValidationError


logger = get_logger("models")


class Token(ResourceModel):
    """
    Token is a resource used to link a :class:`.BankAccount` Or
    :class:`.Card` and a :class:`.Seller` or :class:`.Buyer`.
    https://docs.zoop.co/reference#token-1

    The :attr:`RESOURCE` is used to identify this Model.
    Used to check against :attr:`.resource`!

    It has ``dynamic types``!

    It can be :attr:`CARD_TYPE` or :attr:`BANK_ACCOUNT_TYPE`.

    But before ``creation`` it won't have attribute ``type``.
    So we need to verify by ``other attributes``.
    After ``created`` on Zoop it will have ``type``.

    Attributes:
        token_type (str): value for identified token ``type``

        type (str): optional :attr:`BANK_ACCOUNT_TYPE` or :attr:`CARD_TYPE`.
            It has collision with of :attr:`.BankAccount.type`. So we need the above
            :attr:`token_type`.
        used (bool): optional value of verification

        bank_account (:class:`.BankAccount`): optional value
            (for ``created`` token of 'bank_account' type)
        card (:class:`.Card`): optional value (for ``created`` token of
            'card' type)

        holder_name (str): owner name (for both token of 'bank_account'
            and 'card' type)

        account_number (str): account number for :attr:`BANK_ACCOUNT_TYPE`
        taxpayer_id (str): identifier for :attr:`BANK_ACCOUNT_TYPE` of
            :attr:`.INDIVIDUAL_TYPE`
        ein (str): identifier for :attr:`BANK_ACCOUNT_TYPE` of
            :attr:`.BUSINESS_TYPE`
        bank_code (str): bank code for :attr:`BANK_ACCOUNT_TYPE`
        routing_number (str): agency code in BR for :attr:`BANK_ACCOUNT_TYPE`

        card_number (str): card number for :attr:`CARD_TYPE`
        expiration_month (str): month of expiration for :attr:`CARD_TYPE`
        expiration_year (str): year of expiration for :attr:`CARD_TYPE`
        security_code (str): security code for :attr:`CARD_TYPE`
    """

    RESOURCE = "token"

    CARD_TYPE = "card"
    CARD_IDENTIFIER = "card_number"

    BANK_ACCOUNT_TYPE = "bank_account"
    BANK_ACCOUNT_IDENTIFIER = "bank_code"

    TYPES = {CARD_TYPE, BANK_ACCOUNT_TYPE}
    IDENTIFIERS = {CARD_IDENTIFIER, BANK_ACCOUNT_IDENTIFIER}

    def init_custom_fields(self, type=None, card=None, bank_account=None, **kwargs):
        """
        if ``type`` is :attr:`BANK_ACCOUNT_TYPE` or :attr:`CARD_TYPE`
        token is ``created``!\n
        set :attr:`card` or :attr:`bank_account` attributes accordingly.

        else token is ``not created``!\n
        We must identify token type from attr's passed
        searching for :attr:`CARD_IDENTIFIER` or :attr:`BANK_ACCOUNT_IDENTIFIER`.
        After identifying ``type`` if it was :attr:`BANK_ACCOUNT_TYPE` set ``business``
        or ``individual`` identifier from :class:`.BankAccount` method (which is
        from :class:`.BusinessOrIndividualModel`).

        Args:
            bank_account (dict or :class:`.BankAccount`):  data
            card (dict or :class:`.Card`): data
            type (str): type for ``token`` or ``bank account``
            **kwargs: kwargs
        """

        if type in self.TYPES:
            token_type = type
            if token_type == self.CARD_TYPE:
                setattr(
                    self,
                    self.CARD_TYPE,
                    Card.from_dict_or_instance(card, allow_empty=True),
                )
            else:
                setattr(
                    self,
                    self.BANK_ACCOUNT_TYPE,
                    BankAccount.from_dict_or_instance(bank_account, allow_empty=True),
                )
        else:
            if self.CARD_IDENTIFIER in kwargs:
                token_type = self.CARD_TYPE
            elif self.BANK_ACCOUNT_IDENTIFIER in kwargs:
                token_type = self.BANK_ACCOUNT_TYPE
                BusinessOrIndividualModel.set_identifier(self, **kwargs)
            elif self._allow_empty:
                token_type = None
            else:
                raise ValidationError(
                    self,
                    FieldError(
                        "token_type",
                        f"Tipo de token não identificado! "
                        f"Configure um desses atributos {self.IDENTIFIERS}",
                    ),
                )

        setattr(self, "token_type", token_type)

    def get_bank_account_type(self):
        """
        Get ``bank account type`` for ``creation token`` of :class:`.BankAccount.

        Raises:
            TypeError: when called  from a token not from 'bank_account' type

        Returns:
            value with bank_account type
        """
        if self.token_type == self.BANK_ACCOUNT_TYPE:
            try:
                return self.bank_account.get_type()
            except AttributeError:
                return BankAccount.get_type(self)
        raise TypeError(f"Token is not of type {self.BANK_ACCOUNT_TYPE}")

    def get_validation_fields(self):
        """
        Get ``validation fields`` for instance.\n

        if :attr:`token_type` is :attr:`CARD_TYPE` card return
        :meth:`get_card_required_fields`.

        else :attr:`token_type` is :attr:`BANK_ACCOUNT_TYPE`!
        ``fields`` is :meth:`get_bank_account_required_fields`.\n
        if ``bank account type`` is :attr:`.INDIVIDUAL_TYPE` return ``fields`` union
        :meth:`.get_individual_required_fields`.\n

        else ``bank account type`` is :attr:`.BUSINESS_TYPE` return ``fields`` union
        :meth:`.get_business_required_fields`.

        Returns:
            ``set`` of fields to be validated
        """
        fields = set()

        if self.token_type == self.CARD_TYPE:
            return fields.union(self.get_card_required_fields())
        elif self.token_type == self.BANK_ACCOUNT_TYPE:
            fields = fields.union(self.get_bank_account_required_fields())
            if self.get_bank_account_type() == BankAccount.INDIVIDUAL_TYPE:
                return fields.union(BankAccount.get_individual_required_fields())
            else:
                return fields.union(BankAccount.get_business_required_fields())
        else:
            return fields

    def get_all_fields(self):
        """
        Get ``all fields`` for instance.

        ``fields`` is :meth:`get_validation_fields`

        if :attr:`token_type` is :attr:`CARD_TYPE` return
        ``fields`` union :meth:`get_card_non_required_fields`.

        else :attr:`token_type` is :attr:`BANK_ACCOUNT_TYPE` return
        ``fields`` union :meth:`get_bank_account_non_required_fields`.

        Returns:
            ``set`` of all fields
        """
        fields = self.get_validation_fields()

        if self.token_type == self.CARD_TYPE:
            return fields.union(self.get_card_non_required_fields())
        elif self.token_type == self.BANK_ACCOUNT_TYPE:
            return fields.union(self.get_bank_account_non_required_fields())
        else:
            return fields.union(self.get_non_required_fields())

    def validate_custom_fields(self, **kwargs):
        """
        Valida campos do token.

        Se for um token de cartão, valida o :attr:`.card_number`.

        Args:
            **kwargs:

        Returns:
            Lista com os erros ocorridos (se tiver algum!)
        """

        errors = []
        if self.token_type == self.CARD_TYPE:

            if not validate_card(self.card_number):
                errors.append(
                    FieldError("card_number", "O número do cartão é inválido!")
                )

        return errors

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union({"type", "used"})

    @classmethod
    def get_card_non_required_fields(cls):
        """
        Get ``set`` of ``non required fields`` for :attr:`CARD_TYPE`.

        Returns:
            ``set`` of fields
        """
        fields = cls.get_non_required_fields()
        return fields.union({"card"})

    @classmethod
    def get_card_required_fields(cls):
        """
        Get ``set`` of ``required fields`` for :attr:`CARD_TYPE`.

        Returns:
            ``set`` of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            Card.get_required_fields(), {"card_number", "security_code"}
        )

    @classmethod
    def get_bank_account_non_required_fields(cls):
        """
        Get ``set`` of ``non required fields`` for :attr:`BANK_ACCOUNT_TYPE`

        Returns:
            ``set`` of fields
        """
        fields = cls.get_non_required_fields()
        return fields.union({"bank_account"})

    @classmethod
    def get_bank_account_required_fields(cls):
        """
        get ``set`` of ``required fields`` for :attr:`BANK_ACCOUNT_TYPE`

        Returns:
            ``set`` of fields
        """
        fields = cls.get_required_fields()
        return fields.union({"account_number"})
