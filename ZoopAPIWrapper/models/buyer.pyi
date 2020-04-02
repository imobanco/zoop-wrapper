from typing import Any, Dict

from ZoopAPIWrapper.models.base import FinancialModel as FinancialModel, Person as Person, SocialModel as SocialModel, MarketPlaceModel as MarketPlaceModel


class Buyer(MarketPlaceModel, Person, SocialModel, FinancialModel):
    RESOURCE: str = ...
    default_receipt_delivery_method: Any
    @classmethod
    def get_non_required_fields(cls) -> set: ...
    @classmethod
    def from_dict(cls, data: Dict[str, Any], allow_empty: bool=...) -> Buyer: ...