from typing import Any, Dict

from requests.models import Response

class ZoopResponse(Response):
    data = Dict[str, Any]
