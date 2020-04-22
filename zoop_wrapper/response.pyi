from typing import Any, Optional, Dict, List

from requests.models import Response

from zoop_wrapper.models.base import ResourceModel

class ZoopResponse(Response):
    data = Dict[str, Any]
    instance = Optional[ResourceModel]
    instances = Optional[List[ResourceModel]]
