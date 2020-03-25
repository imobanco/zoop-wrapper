from unittest import TestCase
from unittest.mock import patch, MagicMock


class BuildMockResponseMixin:
    @staticmethod
    def build_response_mock(status_code=200, content=None):
        return MagicMock(
            status_code=status_code,
            json=MagicMock(
                return_value=content if content else {}
            )
        )


class MockedPostDeleteTestCase(TestCase, BuildMockResponseMixin):
    def setUp(self):
        super().setUp()

        self.patcher_post = patch("ZoopAPIWrapper.wrapper.requests.post")
        self.patcher_delete = patch("ZoopAPIWrapper.wrapper.requests.delete")

        self.mocked_post = self.patcher_post.start()
        self.mocked_delete = self.patcher_delete.start()

        self.addCleanup(self.patcher_post.stop)
        self.addCleanup(self.patcher_delete.stop)

    def set_post_mock(self, status_code=200, content=None):
        self.mocked_post.return_value = self.build_response_mock(
            status_code=status_code, content=content
        )

    def set_delete_mock(self, status_code=200, content=None):
        self.mocked_delete.return_value = self.build_response_mock(
            status_code=status_code, content=content
        )
