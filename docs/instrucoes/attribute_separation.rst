Separação de atributos
========================================

Nos nossos `models <https://zoop-wrapper.readthedocs.io/pt_BR/latest/api_ref/models.html>`_ são declarados todos os atributos que a zoop retorna e que podem ser úteis.

Porém nem todos os atributos que a zoop retorna devem ser enviados no método de criação.

.. warning::

    Essa lib não faz a validação de um input que não deveria ser enviado!

Existe apenas a distinção de atributos `required` e `non_required`.

Atributos obrigatórios
-----------------------------------------

Geralmente os atributos `required` são todos os atributos que a zoop precisa receber na criação.

.. note::

    Existem alguns atributos opcionais que estão como `required`. Como por exemplo `Transaction.description`


Atributos opcionais
-----------------------------------------
Já os atributos `non_required` são os que PODEM ser enviados na criação e os atributos que NÃO podem ser enviados na criação.


Atributos de leitura
-----------------------------------------
Não existe essa classificação na lib.

São os atributos que NÃO podem ser enviados na criação. Esses atributos são gerados pela prórpia zoop e retornados pela API deles.

.. warning::

    Atualmente esses atributos estão na lista de `non_required`!

Exemplo de cartão
-----------------------------------------
Na `criação de cartão <https://zoop-wrapper.readthedocs.io/pt_BR/latest/examples/card.html#criar-cartao>`_ enviamos:


.. code-block:: python

    card_token = Token(
        card_number=Faker("credit_card_number").generate(),
        expiration_month="05",
        expiration_year="2030",
        holder_name="foo",
        security_code=123,
    )

e isso nos retorna:

.. code-block:: python

    {
        "id": "4abf4010cc93414ca585463fdc7b44d6",
        "resource": "card",
        "description": null,
        "card_brand": "Visa",
        "first4_digits": "4821",
        "last4_digits": "9566",
        "expiration_month": "5",
        "expiration_year": "2030",
        "holder_name": "foo",
        "is_active": true,
        "is_valid": true,
        "is_verified": false,
        "customer": "0e084bb6a60f47e8ac45949d5040eb92",
        "fingerprint": "e793b5f0ee2362d01d9879d40d99dd9df401c36d735df6b0d34807fcc42c1e6d",
        "address": null,
        "verification_checklist": {
            "postal_code_check": "unchecked",
            "security_code_check": "fail",
            "address_line1_check": "unchecked"
        },
        "metadata": {},
        "uri": "/v1/marketplaces/foo/cards/4abf4010cc93414ca585463fdc7b44d6",
        "created_at": "2020-05-22T15:07:34+00:00",
        "updated_at": "2020-05-22T15:07:35+00:00"
    }

