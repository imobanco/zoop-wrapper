from typing import Any, List

from zoop_wrapper.models.base import (
    FinancialModel as FinancialModel,
    Person as Person,
    SocialModel as SocialModel,
    MarketPlaceModel as MarketPlaceModel,
)


class Buyer(MarketPlaceModel, Person, SocialModel, FinancialModel):
    RESOURCE: str = ...
    default_receipt_delivery_method: Any
    def validate_custom_fields(self, **kwargs) -> List[Any]: ...
    @classmethod
    def get_non_required_fields(cls) -> set: ...
