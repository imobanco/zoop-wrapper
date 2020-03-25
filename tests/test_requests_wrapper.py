from unittest import TestCase
from unittest.mock import MagicMock

from ZoopAPIWrapper.api import RequestsWrapper


class RequestWrapperTestCase(TestCase):
    def setUp(self):
        self.client = RequestsWrapper('url')

    def tearDown(self):
        del self.client

    def test_construct_url(self):
        action = 'teste'
        identifier = '123'

        url = self.client._RequestsWrapper__construct_url(
            action=action,
            identifier=identifier)

        self.assertEqual(url, f'bla/teste/123/')

    def test_process_response(self):
        response = MagicMock(
            content='{"error": {"message": "foo"}}'
        )

        processed_response = self.client.\
            _RequestsWrapper__process_response(response)
        self.assertEqual(processed_response.data, {"error": {"message": "foo"}})
        self.assertEqual(processed_response.error, "foo")

    def test_process_response_resource(self):
        response = MagicMock(
            content='{"resource": "test"}'
        )

        processed_response = self.client.\
            _RequestsWrapper__process_response(response)
        self.assertIsNone(processed_response.instance)

    def test_process_response_resource_list(self):
        response = MagicMock(
            content='{"resource": "list", "items": '
                    '[{"resource": "test", "message": "foo"}]}'
        )

        processed_response = self.client.\
            _RequestsWrapper__process_response(response)
        self.assertEqual(len(processed_response.instances), 1)
        self.assertEqual(processed_response.instances, [None])
