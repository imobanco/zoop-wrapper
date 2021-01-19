import requests

from ..constants import ZOOP_KEY, MARKETPLACE_ID
from ..exceptions import ValidationError
from ..models.base import ZoopObject
from ..utils import get_logger
from ..response import ZoopResponse


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

        Adiciona :attr:`.error` na resposta se tiver ocorrido erros

        Args:
            response (:class:`requests.Response`): resposta a ser processada

        Raises:
            HttpError: quando a resposta não foi ok (200 <= status <= 299)!

        Returns:
            'objeto' (:class:`.ZoopResponse`) de resposta http
        """
        response.data = response.json()

        if response.data.get("error"):
            error = response.data.get("error")

            response.reason = f"{error.get('message')}"
            if error.get("reasons"):
                response.reason += f" {error.get('reasons')}"

            if error.get("status_code"):
                response.status_code = error.get("status_code")

        response.raise_for_status()
        return response

    def _construct_url(
        self,
        action=None,
        identifier=None,
        subaction=None,
        search=None,
        sub_action_before_identifier=False,
    ):
        # noinspection PyProtectedMember
        """
        Constrói a url para o request.

        Args:
            action: nome do resource
            identifier: identificador de detalhe (ID)
            search: query com url args para serem buscados
            sub_action_before_identifier: flag para inverter a posição do identifier e subaction
            subaction: subação do resource

        Examples:
            >>> rw = RequestsWrapper()
            >>> rw._construct_url(action='seller', identifier='1', subaction='bank_accounts', search='account_number=1')  # noqa:
            'rw.__base_url/seller/1/bank_accounts/search?account_number=1'

        Returns:
            url completa para o request
        """
        url = f"{self.__base_url}/"
        if action:
            url += f"{action}/"

        if sub_action_before_identifier:
            if subaction:
                url += f"{subaction}/"
            if identifier:
                url += f"{identifier}/"
        else:
            if identifier:
                url += f"{identifier}/"
            if subaction:
                url += f"{subaction}/"

        if search:
            if isinstance(search, dict):
                url += "?"
                for key, value in search.items():
                    url += f"{key}={value}"
            else:
                url += f"?{search}"
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

    def _post_instance(self, url, instance: ZoopObject):
        """
        http post com instância de um :class:`.ZoopObject`.

        Args:
            url: url da requisição
            instance: instância a ser utilizada

        Raises:
            :class:`.ValidationError`: quando a instância passada não é um :class:`.ZoopObject`.  # noqa

        Returns:
            (:class:`.ZoopResponse`)
        """
        if not isinstance(instance, ZoopObject):
            raise ValidationError(self, "instance precisa ser um ZoopObject!")
        return self._post(url, data=instance.to_dict())

    def _put_instance(self, url, instance: ZoopObject):
        """
        http put com instância de um :class:`.ZoopObject`.

        Args:
            url: url da requisição
            instance: instância a ser utilizada

        Raises:
            :class:`.ValidationError`: quando a instância passada não é um :class:`.ZoopObject`.  # noqa

        Returns:
            (:class:`.ZoopResponse`)
        """
        if not isinstance(instance, ZoopObject):
            raise ValidationError(self, "instance precisa ser um ZoopObject!")
        return self._put(url, data=instance.to_dict())
