from typing import Any, Optional

class BusinessOrIndividualMixin:
    BUSINESS_IDENTIFIER: str = ...
    BUSINESS_TYPE: str = ...
    INDIVIDUAL_IDENTIFIER: str = ...
    INDIVIDUAL_TYPE: str = ...
    URI: dict = ...
    def get_type(self): ...
    def get_type_uri(self): ...
    def set_identifier(self, taxpayer_id: Optional[Any] = ..., ein: Optional[Any] = ...) -> None: ...
