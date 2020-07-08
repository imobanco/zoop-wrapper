from typing import Union

from .base import BaseZoopWrapper
from ..models.webhook import Webhook
from ..response import ZoopResponse


class WebHookWrapper(BaseZoopWrapper):
    """
    Possui os métodos do :class:`.WebHook` e :class:`.Event`

    """

    def add_webhook(self, data: Union[dict, Webhook]) -> ZoopResponse:
        instance = Webhook.from_dict_or_instance(data)
        url = self._construct_url(action="webhooks")
        return self._post_instance(url, instance)

    def list_webhooks(self) -> ZoopResponse:
        url = self._construct_url(action="webhooks")
        return self._get(url)

    def remove_webhook(self, identifier: str) -> ZoopResponse:
        url = self._construct_url(action="webhooks", identifier=identifier)
        return self._delete(url)

    def retrieve_webhook(self, identifier: str) -> ZoopResponse:
        url = self._construct_url(action="webhooks", identifier=identifier)
        return self._get(url)
