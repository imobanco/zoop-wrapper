from ZoopAPIWrapper.models.base import ResourceModel, BusinessOrIndividualModel
from ZoopAPIWrapper.models.bank_account import BankAccount
from ZoopAPIWrapper.models.card import Card
from ZoopAPIWrapper.utils import get_logger


logger = get_logger('models')


class Token(ResourceModel):
    """
    Token is a resource used to link a BankAccount Or Card and a Customer
    https://docs.zoop.co/reference#token-1

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    This has dynamic types!
    It can be 'card' or 'bank_account'.
    But on creation it doesn't have attribute type.
    So we need to verify by other attributes.

    After created it will have 'type'.
    So we need a boolean to control if we get type by other attribute or
    from 'type'.

    Attributes:
        RESOURCE = 'token'

        CARD_TYPE: str 'card' for card type
        CARD_IDENTIFIER: card attribute ('card_number') used to identify type

        BANK_ACCOUNT_TYPE: str 'bank_account' for bank account type
        BANK_ACCOUNT_IDENTIFIER: bank account attribute ('bank_code')
            used to identify type

        TYPES: set of types {CARD_TYPE, BANK_ACCOUNT_TYPE}
        IDENTIFIERS: set of identifiers {CARD_IDENTIFIER,
                                        BANK_ACCOUNT_IDENTIFIER}

        token_type: str for identified token type set by TYPE_ATTR

        type: optional bank_account or card. It has collision with
            BankAccount.type. So we need the above token_type
        used: optional boolean of verification

        bank_account: optional BankAccount instance model
            (for created token of 'bank_account' type)
        card: optional Card instance model (for created token of
            'card' type)

        holder_name: owner name (for both token of 'bank_account'
            and 'card' type)

        account_number: account number of bank account (for token of
            'bank_account' type)
        taxpayer_id: if is for individual bank account (for token of
            'bank_account' type)
        ein: if is for business bank account (for token of 'bank_account' type)
        bank_code: bank code (for token of 'bank_account' type)
        routing_number: agency code in BR (for token of 'bank_account' type)

        expiration_month: month of expiration (for token of 'card' type)
        expiration_year: year of expiration (for token of 'card' type)
        card_number: card number (for token of 'card' type)
        security_code: security code (for token of 'card' type)
    """
    RESOURCE = 'token'

    TYPE_ATTR = 'token_type'

    CARD_TYPE = 'card'
    CARD_IDENTIFIER = 'card_number'

    BANK_ACCOUNT_TYPE = 'bank_account'
    BANK_ACCOUNT_IDENTIFIER = 'bank_code'

    TYPES = {CARD_TYPE, BANK_ACCOUNT_TYPE}
    IDENTIFIERS = {CARD_IDENTIFIER, BANK_ACCOUNT_IDENTIFIER}

    def init_custom_fields(self, type=None, card=None,
                           bank_account=None, **kwargs):
        """
        if type is 'bank_account' or 'card' token is created!
        set card or bank_account attributes accordingly.

        else token is not created!
        we must identify token type from attr's passed
        searching for CARD_IDENTIFIER or BANK_ACCOUNT_IDENTIFIER.
        After identifying type if it was 'bank_account' set business
        or individual identifier from BankAccount method (which is
        from BusinessOrIndividualModel).

        Args:
            type: type for token or bank account
            card: Card instance model or data
            bank_account: BankAccount instance model or data
            **kwargs: kwargs
        """
        if type in self.TYPES:
            token_type = type
            if token_type == self.CARD_TYPE:
                setattr(
                    self, self.CARD_TYPE,
                    Card.from_dict_or_instance(
                        card, allow_empty=True)
                )
            else:
                setattr(
                    self, self.BANK_ACCOUNT_TYPE,
                    BankAccount.from_dict_or_instance(
                        bank_account, allow_empty=True)
                )
        else:
            if self.CARD_IDENTIFIER in kwargs:
                token_type = self.CARD_TYPE
            elif self.BANK_ACCOUNT_IDENTIFIER in kwargs:
                token_type = self.BANK_ACCOUNT_TYPE
                BusinessOrIndividualModel.set_identifier(self, **kwargs)
            else:
                raise TypeError(
                    f'Token type not identified! '
                    f'Please set one of these attributes {self.IDENTIFIERS}')

        setattr(self, 'token_type', token_type)

    def get_type(self):
        """
        get token type value

        Raises:
            TypeError: when token type is not set!

        Returns: str with token type
        """
        try:
            return self.token_type
        except AttributeError as e:
            raise TypeError(
                f'Token type not identified! '
                f'Please set one of these attributes {self.IDENTIFIERS}') from e

    def get_bank_account_type(self):
        """
        get bank account type for creation token of BankAccount

        Raises:
            TypeError: when called  from a token not from 'bank_account' type

        Returns: str with bank_account type
        """
        if self.token_type == self.BANK_ACCOUNT_TYPE:
            try:
                return self.bank_account.get_type()
            except AttributeError:
                return BankAccount.get_type(self)
        raise TypeError(f'Token is not of type {self.BANK_ACCOUNT_TYPE}')

    def get_validation_fields(self):
        """
        get validation fields for types.

        if token is created return bare required_fields.

        elif token type is card return card_required_fields.

        else token type is bank account:
        if bank account is for individual

        Returns: set of fields to be validated
        """
        fields = self.get_required_fields()
        token_type = self.get_type()

        if token_type == self.CARD_TYPE:
            return fields.union(
                self.get_card_required_fields()
            )
        else:
            fields = fields.union(
                self.get_bank_account_required_fields()
            )
            if self.get_bank_account_type() == BankAccount.INDIVIDUAL_TYPE:
                return fields.union(
                    BankAccount.get_individual_required_fields()
                )
            else:
                return fields.union(
                    BankAccount.get_business_required_fields()
                )

    def get_all_fields(self):
        """
        get all fields for types.

        construct set 'fields' from get_validation_fields.

        if token type is card return fields union get_card_non_required_fields.

        else token type is bank account return fields union
        get_bank_account_non_required_fields.

        Returns: set of all fields
        """
        fields = self.get_validation_fields()

        token_type = self.get_type()
        if token_type == self.CARD_TYPE:
            return fields.union(
                self.get_card_non_required_fields()
            )
        else:
            return fields.union(
                self.get_bank_account_non_required_fields()
            )

    @classmethod
    def get_non_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = super().get_non_required_fields()
        return fields.union(
            {'type', 'used'}
        )

    @classmethod
    def get_card_non_required_fields(cls):
        """
        get set of non required fields for 'card' type

        Returns: set of fields
        """
        fields = cls.get_non_required_fields()
        return fields.union(
            {'card'}
        )

    @classmethod
    def get_card_required_fields(cls):
        """
        get set of required fields for 'card' type

        Returns: set of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            Card.get_required_fields(),
            {'card_number', 'security_code'}
        )

    @classmethod
    def get_bank_account_non_required_fields(cls):
        """
        get set of non required fields for 'bank_account' type

        Returns: set of fields
        """
        fields = cls.get_non_required_fields()
        return fields.union(
            {'bank_account'}
        )

    @classmethod
    def get_bank_account_required_fields(cls):
        """
        get set of required fields for 'bank_account' type

        Returns: set of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            {'account_number'}
        )
