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

    Attributes:
        type: bank_account or card
        used: boolean of verification
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
        if type in self.TYPES:
            token_type = type
            self._allow_empty = True
            setattr(self, '_created', True)

            if card is not None and bank_account is not None:
                raise ValueError('this should not happen!')
            elif card is not None:
                setattr(
                    self, self.CARD_TYPE,
                    Card.from_dict_or_instance(card)
                )
            elif bank_account is not None:
                setattr(
                    self, self.BANK_ACCOUNT_TYPE,
                    BankAccount.from_dict_or_instance(bank_account)
                )
            else:
                raise ValueError('this should not happen!')

        else:
            setattr(self, '_created', False)

            if self.CARD_IDENTIFIER in kwargs:
                token_type = self.CARD_TYPE
            elif self.BANK_ACCOUNT_IDENTIFIER in kwargs:
                token_type = self.BANK_ACCOUNT_TYPE
                BusinessOrIndividualModel.set_identifier(self, **kwargs)
            else:
                raise TypeError(
                    f'Token type not identified! '
                    f'Please set one of these attributes {self.IDENTIFIERS}')
        setattr(self, self.TYPE_ATTR, token_type)

    def get_type(self):
        token_type = getattr(
            self, self.TYPE_ATTR, None
        )
        if token_type is None:
            raise TypeError(
                f'Token type not identified! '
                f'Please set one of these attributes {self.IDENTIFIERS}')
        return token_type

    def get_bank_account_type(self):
        if self.token_type == self.BANK_ACCOUNT_TYPE:
            if self._created:
                return self.bank_account.get_type()
            else:
                return BankAccount.get_type(self)
        raise(f'Token is not of type {self.BANK_ACCOUNT_TYPE}')

    def get_validation_fields(self):
        fields = self.get_required_fields()
        token_type = self.get_type()

        if self._created:
            return fields
        elif token_type == self.CARD_TYPE:
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
        fields = cls.get_non_required_fields()
        return fields.union(
            {'card'}
        )

    @classmethod
    def get_card_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union(
            Card.get_required_fields(),
            {'card_number', 'security_code'}
        )

    @classmethod
    def get_bank_account_non_required_fields(cls):
        fields = cls.get_non_required_fields()
        return fields.union(
            {'bank_account'}
        )

    @classmethod
    def get_bank_account_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union(
            {'account_number'}
        )
