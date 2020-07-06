from typing import Union

from requests import HTTPError

from .base import BaseZoopWrapper
from ..exceptions import ValidationError, FieldError


class WebHookWrapper(BaseZoopWrapper):
    """
    Possui os métodos do :class:`.WebHook` e :class:`.Event`

    """

    def list_webhooks(self):
        url = self._construct_url(action='webhooks')
        return self._get(url)

    def remove_webhook(self, identifier):
        url = self._construct_url(action='webhooks', identifier=identifier)
        return self._delete(url)

    def retrieve_webhook(self, identifier):
        url = self._construct_url(action='webhooks', identifier=identifier)
        return self._get(url)
