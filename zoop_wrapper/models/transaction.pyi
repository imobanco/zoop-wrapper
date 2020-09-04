from zoop_wrapper.models.base import (
    ResourceModel as ResourceModel,
    ZoopObject as ZoopObject,
    PaymentMethod as PaymentMethod,
)
from zoop_wrapper.models.card import Card as Card
from zoop_wrapper.models.invoice import Invoice as Invoice
from typing import Any, Optional, Set, List

class PointOfSale(ZoopObject):
    entry_mode: Optional[str]
    identification_number: Optional[Any]
    @classmethod
    def get_non_required_fields(cls): ...

class History(ZoopObject):
    id: Optional[str]
    transaction: Optional[str]
    amount: Optional[str]
    operation_type: Optional[str]
    status: Optional[str]
    response_code: Optional[Any]
    response_message: Optional[Any]
    authorization_code: Optional[Any]
    authorizer_id: Optional[Any]
    authorization_nsu: Optional[Any]
    gatewayResponseTime: Optional[Any]
    authorizer: Optional[Any]
    created_at: Optional[str]
    @classmethod
    def get_non_required_fields(cls): ...

class Transaction(ResourceModel):
    RESOURCE: str = ...
    CARD_TYPE: str = ...
    BOLETO_TYPE: str = ...
    PAYMENT_TYPES: Set[str] = ...

    amount: str
    currency: str
    description: str
    on_behalf_of: str
    customer: str
    payment_type: str
    payment_method: PaymentMethod

    reference_id: Optional[str]
    status: Optional[str]
    confirmed: Optional[str]
    original_amount: Optional[str]
    transaction_number: Optional[set]
    gateway_authorizer: Optional[Any]
    app_transaction_uid: Optional[Any]
    refunds: Optional[Any]
    rewards: Optional[Any]
    discounts: Optional[Any]
    pre_authorization: Optional[Any]
    sales_receipt: Optional[Any]
    statement_descriptor: Optional[str]
    installment_plan: Optional[Any]
    refunded: Optional[bool]
    voided: Optional[bool]
    captured: Optional[bool]
    fees: Optional[Any]
    fee_details: Optional[Any]
    location_latitude: Optional[Any]
    location_longitude: Optional[Any]
    individual: Optional[Any]
    business: Optional[Any]
    expected_on: Optional[str]
    point_of_sale: Optional[PointOfSale]
    history: Optional[List[History]]
    def init_custom_fields(
        self,
        payment_type: Optional[Any] = ...,
        payment_method: Optional[Any] = ...,
        point_of_sale: Optional[Any] = ...,
        history: Optional[Any] = ...,
        currency: str = ...,
        **kwargs: Any,
    ) -> None: ...
    def get_validation_fields(self): ...
    def get_all_fields(self): ...
    @classmethod
    def get_required_fields(cls): ...
    @classmethod
    def get_card_required_fields(cls): ...
    @classmethod
    def get_boleto_required_fields(cls): ...
    @classmethod
    def get_non_required_fields(cls): ...

class Source(ZoopObject):
    CARD_PRESENT_TYPE: str = ...
    CARD_NOT_PRESENT_TYPE: str = ...
    SOURCE_TYPES: Any = ...

    type: str = ...
    card: str = ...
    card_type: str = ...
    amount: str = ...
    currency: str = ...
    usage: str = ...
    def init_custom_fields(
        self, card: Optional[Any] = ..., type: str = ..., **kwargs: Any
    ) -> None: ...
    def get_validation_fields(self): ...
    def get_all_fields(self): ...
    @classmethod
    def get_required_fields(cls): ...
    @classmethod
    def get_card_not_present_required_fields(cls): ...
    @classmethod
    def get_card_present_required_fields(cls): ...

class InstallmentPlan(ZoopObject):
    INTEREST_FREE_MODE: str = ...
    WITH_INTEREST_MODE: str = ...
    INSTALLMENT_PLAN_MODES: Any = ...

    mode: str = ...
    installment_number: int = ...
    def get_required_fields(cls): ...
    @classmethod
    def validate_custom_fields(cls, **kwargs: Any) -> List[Any]: ...
    @classmethod
    def _validate_number_installments(cls, number_installments: Any) -> bool: ...
