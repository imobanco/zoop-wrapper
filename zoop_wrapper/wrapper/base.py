import requests

from zoop_wrapper.constants import ZOOP_KEY, MARKETPLACE_ID
from zoop_wrapper.models.base import ResourceModel
from zoop_wrapper.models.utils import get_instance_from_data
from zoop_wrapper.utils import get_logger, config_logging
from zoop_wrapper.response import ZoopResponse


config_logging()
logger = get_logger("wrapper")


class RequestsWrapper:
    """
    wrapper da lib requests

    Attributes:
        __base_url: Url base para construir os requests
    """

    def __init__(self, base_url):
        self.__base_url = base_url

    @staticmethod
    def __process_response(response) -> ZoopResponse:
        """
        Processa a resposta.

        Adiciona o :attr:`.data` carregado do :meth:`requests.Response.json`.

        Adiciona o :attr:`.instance` ou :attr:`.instances` baseado no resource.

        .. note::
            Apenas adiciona :attr:`.instance` ou :attr:`.instances` se não tiver o dado 'deleted' no :attr:`.data`
            que é retornado em todas as respostas de deleção (200 ok) e se tiver o dado `resource` no :attr:`.data`

        Adiciona :attr:`.error` na resposta se tiver ocorrido erros

        Args:
            response (:class:`.Response`): objeto de resposta http

        Raises:
            HttpError: quando a resposta não foi ok (200 <= status <= 299)!

        Returns:
            objeto (:class:`.ZoopResponse`) de resposta http
        """
        response.data = response.json()

        deleted = response.data.get("deleted")
        if not deleted:
            resource = response.data.get("resource")
            if resource == "list":
                response.instances = [
                    get_instance_from_data(item) for item in response.data.get("items")
                ]
            elif resource is not None:
                response.instance = get_instance_from_data(response.data)

        if response.data.get("error"):
            error = response.data.get("error")

            response.reason = f"{error.get('message')}"
            if error.get("reasons"):
                response.reason += f" {error.get('reasons')}"

            if error.get("status_code"):
                response.status_code = error.get("status_code")

        response.raise_for_status()
        return response

    def _construct_url(self, action=None, identifier=None, subaction=None, search=None):
        # noinspection PyProtectedMember
        """
        construct url for the request

        Args:
            action: action endpoint
            identifier: identifier detail string (ID)
            subaction: subaction endpoint
            search: query with urls args to be researched

        Examples:
            >>> rw = RequestsWrapper()
            >>> rw._construct_url(action='seller', identifier='1', subaction='bank_accounts', search='account_number=1')  # noqa:
            'rw.__base_url/seller/1/bank_accounts/search?account_number=1'

        Returns:
            full url for the request
        """
        url = f"{self.__base_url}/"
        if action:
            url += f"{action}/"
        if identifier:
            url += f"{identifier}/"
        if subaction:
            url += f"{subaction}/"
        if search:
            url += f"search?{search}"
        return url

    @property
    def _auth(self):
        """
        Propriedade de autenticação

        Raises:
            NotImplementedError: É um método abstrato!
        """
        raise NotImplementedError("Must implement auth function!")

    def _delete(self, url) -> ZoopResponse:
        """
        http delete

        Args:
            url: url de requisição

        Returns:
            (:class:`.ZoopResponse`)
        """
        response = requests.delete(url, auth=self._auth)
        # noinspection PyTypeChecker
        response = self.__process_response(response)
        return response

    def _get(self, url) -> ZoopResponse:
        """
        http get

        Args:
            url: url de requisição

        Returns:
            (:class:`.ZoopResponse`)
        """
        response = requests.get(url, auth=self._auth)
        # noinspection PyTypeChecker
        response = self.__process_response(response)
        return response

    def _post(self, url, data) -> ZoopResponse:
        """
        http post

        Args:
            url: url de requisição
            data (dict): dados da requisição

        Returns:
            (:class:`.ZoopResponse`)
        """
        response = requests.post(url, json=data, auth=self._auth)
        # noinspection PyTypeChecker
        response = self.__process_response(response)
        return response

    def _put(self, url, data) -> ZoopResponse:
        """
        http put

        Args:
            url: url de requisição
            data (dict): dados da requisição

        Returns:
            (:class:`.ZoopResponse`)
        """
        response = requests.put(url, json=data, auth=self._auth)
        # noinspection PyTypeChecker
        response = self.__process_response(response)
        return response


class BaseZoopWrapper(RequestsWrapper):
    """
    wrapper da Zoop API

    Attributes:
        __marketplace_id: marketplace id da zoop
        __key: chave de autenticação da zoop
    """

    BASE_URL = "https://api.zoop.ws/v1/marketplaces/"

    def __init__(self, marketplace_id=None, key=None):
        if marketplace_id is None:
            marketplace_id = MARKETPLACE_ID

        if key is None:
            key = ZOOP_KEY

        self.__marketplace_id = marketplace_id
        self.__key = key

        super().__init__(base_url=f"{self.BASE_URL}{self.__marketplace_id}")

    @property
    def _auth(self):
        """
        Propriedade de autenticação.

        :getter: Returns this direction's name

        Returns:
            tupla com :attr:`.ZoopKey` e ""
        """
        return self.__key, ""

    def _post_instance(self, url, instance: ResourceModel):
        """
        http post com instância de um :class:`.ResourceModel`.

        Args:
            url: url da requisição
            instance: instância a ser utilizada

        Raises:
            :class:`.ValidationError`: quando a instância passada não é um :class:`.ResourceModel`.

        Returns:
            (:class:`.ZoopResponse`)
        """
        if not isinstance(instance, ResourceModel):
            raise TypeError("instance must be a ZoopModel")
        return self._post(url, data=instance.to_dict())
