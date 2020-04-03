from unittest import TestCase
from unittest.mock import patch, MagicMock

from requests import Response
from ZoopAPIWrapper.wrapper import ZoopWrapper


class SetTestCase(TestCase):
    @staticmethod
    def __get_msg(container, contained):
        return f'\n\nset {container} does not contains {contained}.\n\n' \
               f'Excess: {contained - container}'

    def assertIsSubSet(self, contained: set, container: set):
        self.assertTrue(
            contained.issubset(container),
            msg=self.__get_msg(container, contained)
        )


class MockedLoggerTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.patcher_address_loggger = patch(
            "ZoopAPIWrapper.models.base.logger")
        self.patcher_wrapper_loggger = patch(
            "ZoopAPIWrapper.wrapper.logger")

        self.mocked_address_logger = self.patcher_address_loggger.start()
        self.mocked_wrapper_logger = self.patcher_wrapper_loggger.start()

        self.addCleanup(self.patcher_address_loggger.stop)
        self.addCleanup(self.patcher_wrapper_loggger.stop)


class APITestCase(MockedLoggerTestCase):
    def setUp(self):
        super().setUp()

        self.patcher_get = patch("ZoopAPIWrapper.wrapper.requests.get")
        self.patcher_post = patch("ZoopAPIWrapper.wrapper.requests.post")
        self.patcher_delete = patch("ZoopAPIWrapper.wrapper.requests.delete")

        self.mocked_get = self.patcher_get.start()
        self.mocked_post = self.patcher_post.start()
        self.mocked_delete = self.patcher_delete.start()

        self.addCleanup(self.patcher_get.stop)
        self.addCleanup(self.patcher_post.stop)
        self.addCleanup(self.patcher_delete.stop)

        self.client = ZoopWrapper()

    def tearDown(self):
        super().tearDown()
        del self.client

    @staticmethod
    def build_response_mock(status_code=200, content=None):
        response = MagicMock(
            status_code=status_code,
            json=MagicMock(
                return_value=content if content else {}
            ),
            instance=None
        )

        def raise_for_status():
            Response.raise_for_status(response)

        response.raise_for_status = raise_for_status
        return response

    def set_get_mock(self, status_code=200, content=None):
        self.mocked_get.return_value = self.build_response_mock(
            status_code=status_code, content=content
        )

    def set_post_mock(self, status_code=200, content=None):
        self.mocked_post.return_value = self.build_response_mock(
            status_code=status_code, content=content
        )

    def set_delete_mock(self, status_code=200, content=None):
        self.mocked_delete.return_value = self.build_response_mock(
            status_code=status_code, content=content
        )
