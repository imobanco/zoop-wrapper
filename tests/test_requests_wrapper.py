from unittest.mock import patch

from tests.utils import APITestCase
from ZoopAPIWrapper.wrapper import RequestsWrapper


class RequestWrapperTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = RequestsWrapper('foo')

    def test_construct_url(self):
        action = 'teste'
        identifier = '123'

        url = self.client._construct_url(
            action=action,
            identifier=identifier)

        self.assertEqual(url, f'foo/teste/123/')

    @patch('ZoopAPIWrapper.wrapper.logger')
    def test_process_response_error(self, mocked_logger):
        response = self.build_response_mock(
            content={"error": {"message": "foo"}})

        processed_response = self.client.\
            _RequestsWrapper__process_response(response)
        self.assertEqual(processed_response.data, {"error": {"message": "foo"}})
        self.assertEqual(processed_response.reason, "foo")

    @patch('ZoopAPIWrapper.wrapper.logger')
    def test_process_response_error_reasons(self, mocked_logger):
        response = self.build_response_mock(
            content={"error": {"message": "foo", "reasons": ['bla bla bla']}})

        processed_response = self.client.\
            _RequestsWrapper__process_response(response)
        self.assertEqual(
            processed_response.data,
            {"error": {"message": "foo", "reasons": ['bla bla bla']}})
        self.assertEqual(processed_response.reason, "foo ['bla bla bla']")

    def test_process_response_resource(self):
        response = self.build_response_mock(content={"resource": "test"})

        processed_response = self.client.\
            _RequestsWrapper__process_response(response)
        self.assertIsNone(processed_response.instance)

    def test_process_response_resource_list(self):
        response = self.build_response_mock(
            content={"resource": "list", "items": [
                {"resource": "test", "message": "foo"}]}
        )

        processed_response = self.client.\
            _RequestsWrapper__process_response(response)
        self.assertEqual(len(processed_response.instances), 1)
        self.assertEqual(processed_response.instances, [None])
