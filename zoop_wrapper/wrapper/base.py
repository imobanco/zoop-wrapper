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
    requests lib wrapper

    Attributes:
        __base_url: base url to construct requests
    """

    def __init__(self, base_url):
        self.__base_url = base_url

    @staticmethod
    def __process_response(response) -> ZoopResponse:
        """
        add 'data' attribute to response from json content of response.

        add 'instance' or 'instances' attribute to response by resource.
        Only add 'instance' or 'instances' if there's no `deleted` attribute
        which is set on all delete response (200 ok) and if there's the
        `resource` attribute on response

        add 'error' attribute to response if had errors

        Args:
            response: http response

        Raises:
            HttpError: when response is not ok!

        Returns:
            processed http response
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
        property of authentication

        Raises:
            NotImplementedError: it's a abstract method
        """
        raise NotImplementedError("Must implement auth function!")

    def _get(self, url) -> ZoopResponse:
        """
        http get request wrapper

        Args:
            url: url to be requested

        Returns:
            processed response
        """
        response = requests.get(url, auth=self._auth)
        # noinspection PyTypeChecker
        response = self.__process_response(response)
        return response

    def _post(self, url, data) -> ZoopResponse:
        """
        http post request wrapper

        Args:
            url: url to be requested
            data: data to be posted

        Returns:
            processed response
        """
        response = requests.post(url, json=data, auth=self._auth)
        # noinspection PyTypeChecker
        response = self.__process_response(response)
        return response

    def _delete(self, url) -> ZoopResponse:
        """
        http delete request wrapper

        Args:
            url: url to be requested

        Returns:
            processed response
        """
        response = requests.delete(url, auth=self._auth)
        # noinspection PyTypeChecker
        response = self.__process_response(response)
        return response


class BaseZoopWrapper(RequestsWrapper):
    """
    Zoop API methods wrapper

    Attributes:
        __marketplace_id: marketplace id from zoop for the zoop account
        __key: zoop auth token
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
        property of authentication

        Returns:
            tuple with ZoopKey
        """
        return self.__key, ""

    def _post_instance(self, url, instance: ResourceModel):
        """
        http post request wrapper with instance

        Args:
            url: url to be requested
            instance: instance to be posted

        Returns:
            processed response
        """
        if not isinstance(instance, ResourceModel):
            raise TypeError("instance must be a ZoopModel")
        return self._post(url, data=instance.to_dict())
