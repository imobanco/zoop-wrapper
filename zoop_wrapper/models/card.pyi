from zoop_wrapper.models.base import PaymentMethod as PaymentMethod, VerificationModel as VerificationModel
from typing import Any, Optional, Union, Dict

class CardVerificationChecklist(VerificationModel):
    security_code_check: Optional[bool]
    @classmethod
    def get_required_fields(cls) -> set: ...

class Card(PaymentMethod):
    RESOURCE: str = ...

    expiration_month: str
    expiration_year: str
    holder_name: str

    card_brand: Optional[str]
    first4_digits: Optional[str]
    last4_digits:Optional[ str]
    is_active: Optional[bool]
    is_valid: Optional[bool]
    is_verified: Optional[bool]
    fingerprint: Optional[str]
    verification_checklist: Optional[CardVerificationChecklist]
    def init_custom_fields(self, verification_checklist: Optional[Union[Dict[str, bool], VerificationModel]] = ..., **kwargs: Any) -> None: ...  # type: ignore
    @classmethod
    def get_required_fields(cls) -> set: ...
    @classmethod
    def get_non_required_fields(cls) -> set: ...
