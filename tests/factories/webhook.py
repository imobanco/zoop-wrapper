from factory import LazyFunction
from factory.faker import Faker

from .base import ResourceModelFactory
from zoop_wrapper.models.webhook import Webhook


class WebhookFactory(ResourceModelFactory):
    class Meta:
        model = Webhook

    resource = 'webhook'

    method = "POST"
    url = Faker('uri')
    events = LazyFunction(lambda: [Faker('random_element', elements=Webhook.EVENTS).generate()])
    description = Faker("sentence", nb_words=5)
