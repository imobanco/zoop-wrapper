from logging import Logger
from ZoopAPIWrapper.models.base import ZoopModel
from typing import Any, List

logger: Logger
RESOURCE_CLASSES: List[ZoopModel]
RESOURCES_DICT: dict

def get_instance_from_data(data: Any): ...
