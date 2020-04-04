from ZoopAPIWrapper.models.base import (
    ZoopBase, ZoopModel)


class PointOfSale(ZoopBase):
    __FIELDS = ['entry_mode', 'identification_number']

    def __init__(self, entry_mode,
                 identification_number=None,
                 **kwargs):
        super().__init__(**kwargs)

        self.entry_mode = entry_mode
        self.identification_number = identification_number

    @property
    def fields(self):
        """
        the fields of ZoopBase are it's
        __FIELDS extended with it's father fields.
        it's important to be a new list (high order function)
        Returns: new list of attributes
        """
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class Transaction(ZoopModel):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        security_code_check: boolean of verification
    """
    RESOURCE = 'transaction'

    __FIELDS = []

    {
        "id": "08888da036fd4c5e8491550881e44e94",
        "resource": "transaction",
        "status": "pending",
        "confirmed": "0",
        "amount": "20.00",
        "original_amount": "20.00",
        "currency": "BRL",
        "description": "celular",
        "payment_type": "boleto",
        "transaction_number": null,
        "gateway_authorizer": null,
        "app_transaction_uid": null,
        "refunds": null,
        "rewards": null,
        "discounts": null,
        "pre_authorization": null,
        "sales_receipt": null,
        "on_behalf_of": "d6940dbb811846fda1544d39d2fe7463",
        "customer": "d38a99b734fb4a0f9a0bd92499aab9f5",
        "statement_descriptor": "bemvindo",
        "payment_method",
        "point_of_sale",
        "installment_plan": null,
        "refunded": false,
        "voided": false,
        "captured": true,
        "fees": "0.00",
        "fee_details": null,
        "location_latitude": null,
        "location_longitude": null,
        "individual": null,
        "business": null,
        "uri": "/v1/marketplaces/d77c2258b51d49269191502695f939f4/transactions/08888da036fd4c5e8491550881e44e94",
        "metadata": {},
        "expected_on": "2019-02-19T13:05:28+00:00",
        "created_at": "2019-02-19T16:05:28+00:00",
        "updated_at": "2019-02-19T16:05:28+00:00",
        "history": [
            {
                "id": "3781c72add004feaae74942c7acda859",
                "transaction": "08888da036fd4c5e8491550881e44e94",
                "amount": "20.00",
                "operation_type": "created",
                "status": "succeeded",
                "response_code": null,
                "response_message": null,
                "authorization_code": null,
                "authorizer_id": null,
                "authorization_nsu": null,
                "gatewayResponseTime": null,
                "authorizer": null,
                "created_at": "2019-02-19 16:05:28"
            }
        ]
    },