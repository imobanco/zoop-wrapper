Entrada de dados
========================================

As entradas de dados podem ser feitas utilizando os `models <https://zoop-wrapper.readthedocs.io/pt_BR/latest/api_ref/models.html>`_ Python declarados na lib ou dicionários Python.

Nos exemplos documentados utilizaremos os models declarados, mas pode ser utilizados dict's ao invés.

Por exemplo na `criação de uma transação de cartão presente <https://zoop-wrapper.readthedocs.io/pt_BR/latest/examples/transaction.html#criar-transacao-de-cartao-de-credito-presente>`_ poderia ter sido utilizado o seguinte dicionário:

.. code-block:: python

    t = {
        "customer": seller_brian,
        "description": "Uma descrição breve da motivação da sua transação",
        "on_behalf_of": seller_denise,
        "payment_type": "credit",
        "source": {
            "amount": "1234",
            "card": {
                "card_number": Faker("credit_card_number").generate(),
                "expiration_month": "05",
                "expiration_year": "2030",
                "holder_name": "foo",
                "security_code": 123,
            },
            "usage": "single_use",
        },
    }