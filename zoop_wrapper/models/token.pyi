from zoop_wrapper.models.bank_account import BankAccount as BankAccount
from zoop_wrapper.models.base import (
    BusinessOrIndividualModel as BusinessOrIndividualModel,
    ResourceModel as ResourceModel,
)
from zoop_wrapper.models.card import Card as Card
from zoop_wrapper.utils import get_logger as get_logger
from typing import Any, Optional, Set, Dict, Union

logger: Any

class Token(ResourceModel):
    RESOURCE: str = ...
    TYPE_ATTR: str = ...
    CARD_TYPE: str = ...
    CARD_IDENTIFIER: str = ...
    BANK_ACCOUNT_TYPE: str = ...
    BANK_ACCOUNT_IDENTIFIER: str = ...
    TYPES: Set[str] = ...
    IDENTIFIERS: Set[str] = ...

    _created: bool
    token_type: str

    type: Optional[str]
    used: Optional[bool]

    bank_account: Optional[BankAccount]
    card: Optional[Card]

    holder_name: Optional[str]

    account_number: Optional[str]
    taxpayer_id: Optional[str]
    ein: Optional[str]
    bank_code: Optional[str]
    routing_number: Optional[str]

    expiration_month: Optional[str]
    expiration_year: Optional[str]
    card_number: Optional[str]
    security_code: Optional[str]
    def init_custom_fields(
        self,
        type: Optional[Any] = ...,
        card: Optional[Any] = ...,
        bank_account: Optional[Any] = ...,
        **kwargs: Any,
    ) -> None: ...
    def get_bank_account_type(self): ...
    def get_validation_fields(self): ...
    def get_all_fields(self): ...
    @classmethod
    def get_non_required_fields(cls): ...
    @classmethod
    def get_card_non_required_fields(cls): ...
    @classmethod
    def get_card_required_fields(cls): ...
    @classmethod
    def get_bank_account_non_required_fields(cls): ...
    @classmethod
    def get_bank_account_required_fields(cls): ...
    @classmethod
    def from_dict_or_instance(cls, data: Union[Dict[str, Any], Token], allow_empty: bool = ..., **kwargs: Any) -> Token: ...  # type: ignore
