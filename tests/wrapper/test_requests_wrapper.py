from requests.exceptions import HTTPError

from tests.utils import APITestCase
from zoop_wrapper.wrapper.base import RequestsWrapper


class RequestWrapperTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = RequestsWrapper("foo")

    def test_construct_url_action(self):
        action = "teste"

        url = self.client._construct_url(action=action)

        self.assertEqual(url, "foo/teste/")

    def test_construct_url_action_identifier(self):
        identifier = "123"

        url = self.client._construct_url(identifier=identifier)

        self.assertEqual(url, "foo/123/")

    def test_construct_url_subaction(self):
        subaction = "bar"

        url = self.client._construct_url(subaction=subaction)

        self.assertEqual(url, "foo/bar/")

    def test_construct_url_subaction_identifier(self):
        identifier = "123"
        subaction = "bar"

        url = self.client._construct_url(identifier=identifier, subaction=subaction)

        self.assertEqual(url, "foo/123/bar/")

    def test_construct_url_subaction_identifier_inverted(self):
        identifier = "123"
        subaction = "bar"

        url = self.client._construct_url(
            identifier=identifier,
            subaction=subaction,
            sub_action_before_identifier=True,
        )

        self.assertEqual(url, "foo/bar/123/")

    def test_construct_url_search(self):
        search = "id=1"

        url = self.client._construct_url(search=search)

        self.assertEqual(url, "foo/?id=1")

    def test_construct_url_search_dict(self):
        search = {"id": 1}

        url = self.client._construct_url(search=search)

        self.assertEqual(url, "foo/?id=1")

    def test_process_response_error(self):
        response = self.build_response_mock(
            status_code=400, content={"error": {"message": "foo", "status_code": 400}}
        )

        self.assertRaises(
            HTTPError, self.client._RequestsWrapper__process_response, response
        )
        self.assertEqual(
            response.data, {"error": {"message": "foo", "status_code": 400}}
        )
        self.assertEqual(response.reason, "foo")

    def test_process_response_200_error(self):
        response = self.build_response_mock(
            status_code=200, content={"error": {"message": "foo", "status_code": 400}}
        )

        self.assertRaises(
            HTTPError, self.client._RequestsWrapper__process_response, response
        )
        self.assertEqual(
            response.data, {"error": {"message": "foo", "status_code": 400}}
        )
        self.assertEqual(response.reason, "foo")

    def test_process_response_error_reasons(self):
        response = self.build_response_mock(
            content={"error": {"message": "foo", "reasons": ["bla bla bla"]}}
        )

        processed_response = self.client._RequestsWrapper__process_response(response)
        self.assertEqual(
            processed_response.data,
            {"error": {"message": "foo", "reasons": ["bla bla bla"]}},
        )
        self.assertEqual(processed_response.reason, "foo ['bla bla bla']")
