from ..utils import APITestCase
from ..factories.webhook import WebhookFactory
from zoop_wrapper.models.webhook import Webhook


class WebhookWrapperTestCase(APITestCase):
    def test_add_webhook(self):
        self.set_post_mock(201, WebhookFactory().to_dict())

        data = {
            "description": "asd",
            "url": "http://google.com",
            "method": "POST",
            "events": ["document.created", "document.updated"],
        }

        response = self.client.add_webhook(data)
        self.assertEqual(response.status_code, 201, msg=response.data)

        expected_data = Webhook.from_dict(data).to_dict()

        self.mocked_post.assert_called_once_with(
            f"{self.base_url}/webhooks/", json=expected_data, auth=self.auth
        )

    def test_list_webhooks(self):
        self.set_get_mock(200, {"items": [WebhookFactory()]})

        response = self.client.list_webhooks()
        self.assertEqual(response.status_code, 200, msg=response.data)

        self.mocked_get.assert_called_once_with(
            f"{self.base_url}/webhooks/", auth=self.auth
        )

    def test_retrieve_webhook(self):
        self.set_get_mock(200, WebhookFactory(id="foo").to_dict())

        response = self.client.retrieve_webhook("foo")
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get("id"), "foo")
        self.assertIsInstance(response.instance, Webhook)
        self.assertEqual(response.instance.id, "foo")

        self.mocked_get.assert_called_once_with(
            f"{self.base_url}/webhooks/foo/", auth=self.auth
        )

    def test_remove_webhook(self):
        """
        A api da zoop retorna 200 com esse payload em um request DELETE
        """
        self.set_delete_mock(200, {"id": "foo", "resource": "webhook", "deleted": True})

        response = self.client.remove_webhook("foo")
        self.assertEqual(response.status_code, 200, msg=response.data)

        self.mocked_delete.assert_called_once_with(
            f"{self.base_url}/webhooks/foo/", auth=self.auth
        )
