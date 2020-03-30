from ZoopAPIWrapper.models.base import ResourceModel as ResourceModel

class Token(ResourceModel):
    RESOURCE: str = ...
    type: str
    used: str
    @classmethod
    def get_non_required_fields(cls) -> set: ...
