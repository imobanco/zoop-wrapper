from .base import ZoopObject, ResourceModel
from ..exceptions import FieldError


class Event(ResourceModel):
    """
    Evento assíncrono enviado pela Zoop.

    https://docs.zoop.co/docs/sobre-os-webhooks#corpo-de-um-evento
    https://docs.zoop.co/docs/eventos-dispon%C3%ADveis
    """

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union({"payload"})


class Webhook(ZoopObject):
    """
    Webhook para cadastro de eventos assíncronos enviados pela Zoop.

    https://docs.zoop.co/reference#webhook
    """

    EVENTS = {
        "buyer.transaction.canceled",
        "buyer.transaction.charged_back",
        "buyer.transaction.commission.succeeded",
        "buyer.transaction.created",
        "buyer.transaction.dispute.succeeded",
        "buyer.transaction.disputed",
        "buyer.transaction.failed",
        "buyer.transaction.pre_authorized",
        "buyer.transaction.reversed",
        "buyer.transaction.succeeded",
        "buyer.transaction.updated",
        "document.created",
        "document.updated",
        "invoice.canceled",
        "invoice.created",
        "invoice.expired",
        "invoice.overdue",
        "invoice.paid",
        "invoice.refunded",
        "invoice.updated",
        "plan.created",
        "plan.deleted",
        "plan.updated",
        "seller.activated",
        "seller.created",
        "seller.deleted",
        "seller.denied",
        "seller.enabled",
        "seller.tef.disable",
        "seller.tef.enable",
        "seller.tef.pending",
        "seller.updated",
        "subscription.active",
        "subscription.canceled",
        "subscription.created",
        "subscription.deleted",
        "subscription.expired",
        "subscription.overdue",
        "transaction.authorization.failed",
        "transaction.authorization.succeeded",
        "transaction.canceled",
        "transaction.capture.failed",
        "transaction.capture.succeeded",
        "transaction.charged_back",
        "transaction.commission.succeeded",
        "transaction.created",
        "transaction.dispute.succeeded",
        "transaction.disputed",
        "transaction.pre_authorization.failed",
        "transaction.pre_authorization.succeeded",
        "transaction.pre_authorized",
        "transaction.reversed",
        "transaction.succeeded",
        "transaction.updated",
        "transaction.void.failed",
        "transaction.void.succeeded"
    }

    def init_custom_fields(self, method="POST", events=None, **kwargs) -> None:
        setattr(self, 'method', method)

        if events is None:
            setattr(self, 'events', [])
        elif not isinstance(events, list):
            setattr(self, 'events', [events])

    def validate_custom_fields(self, **kwargs):
        errors = []

        events_set = set(self.events)
        if set().issuperset(events_set):
            errors.append(
                FieldError('events', 'A lista de eventos não pode ser vazia')
            )
        elif not events_set.issubset(self.EVENTS):
            errors.append(
                FieldError(
                    'events',
                    f'Os eventos {events_set-self.EVENTS} não são válidos! \n'
                    f'Os possíveis eventos são: {self.EVENTS}'
                )
            )

        return errors

    @classmethod
    def get_required_fields(cls) -> set:
        fields = super().get_required_fields()
        return fields.union({"method", "url", "events"})

    @classmethod
    def get_non_required_fields(cls) -> set:
        fields = super().get_non_required_fields()
        return fields.union({"description"})
