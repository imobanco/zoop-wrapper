from logging import Logger
from ZoopAPIWrapper.models.base import ResourceModel
from typing import Any, List, Dict, Union

logger: Logger
RESOURCE_CLASSES: List[ResourceModel]
RESOURCES_DICT: Dict[str, ResourceModel]

def _get_model_class_from_resource(resource: str) -> ResourceModel: ...

def get_instance_from_data(data: Dict[str, Any]) -> Union[ResourceModel, None]: ...
