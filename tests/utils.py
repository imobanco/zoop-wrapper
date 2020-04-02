from unittest import TestCase
from unittest.mock import patch, MagicMock


class SetTestCase(TestCase):
    @staticmethod
    def __get_msg(container, contained):
        return f'set {container} does not contains {contained}'

    def assertIsSubSet(self, contained: set, container: set):
        self.assertTrue(
            contained.issubset(container),
            msg=self.__get_msg(container, contained)
        )

    def assertIsSuperSet(self, container: set, contained: set):
        self.assertTrue(
            container.issuperset(contained),
            msg=self.__get_msg(container, contained)
        )


class BuildResponseMockMixin:
    @staticmethod
    def build_response_mock(status_code=200, content=None):
        return MagicMock(
            status_code=status_code,
            json=MagicMock(
                return_value=content if content else {}
            ),
            instance=None
        )


class MockedAddressLoggerTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.patcher_address_loggger = patch(
            "ZoopAPIWrapper.models.base.logger")

        self.mocked_address_logger = self.patcher_address_loggger.start()

        self.addCleanup(self.patcher_address_loggger.stop)


class RequestsMockedTestCase(MockedAddressLoggerTestCase,
                             BuildResponseMockMixin):
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
