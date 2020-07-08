from typing import Union

from .base import BaseZoopWrapper
from ..models.webhook import Webhook
from ..response import ZoopResponse


class WebhookWrapper(BaseZoopWrapper):
    """
    Possui os métodos do :class:`.WebHook` e :class:`.Event`

    """

    def add_webhook(self, data: Union[dict, Webhook]) -> ZoopResponse:
        """
        Adiciona um novo webhook no marketplace da zoop.

        Args:
            data: dicionário ou instância de dados

        Returns:
            :class:`.ZoopResponse` com a instância
        """
        instance = Webhook.from_dict_or_instance(data)
        url = self._construct_url(action="webhooks")
        return self._post_instance(url, instance)

    def list_webhooks(self) -> ZoopResponse:
        """
        Lista todos os webhooks do marketplace na zoop.

        Returns:
            :class:`.ZoopResponse` com as instâncias
        """
        url = self._construct_url(action="webhooks")
        return self._get(url)

    def remove_webhook(self, identifier: str) -> ZoopResponse:
        """
        Remove/deleta um webhook do marketplace na zoop.

        Args:
            identifier: id na zoop do webhook

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="webhooks", identifier=identifier)
        return self._delete(url)

    def retrieve_webhook(self, identifier: str) -> ZoopResponse:
        """
        Retorna um webhook do marketplace na zoop.

        Args:
            identifier: id na zoop do webhook

        Returns:
            :class:`.ZoopResponse` com a instância
        """
        url = self._construct_url(action="webhooks", identifier=identifier)
        return self._get(url)
