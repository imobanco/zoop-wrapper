Eventos de Transação
========================================

No mundo de transações, existem alguns eventos. Dentro deles temos por exemplo::

    - success
    - failed
    - canceled
    - reversed
    - charged_back
    - pre_authorized
    - captured
    - voided


Charge Back
***********************************
Processo no qual o gateway de pagamento cobra um vendedor o valor da compra pago pelo comprador.
Retornando o dinheiro ao comprador.

Void
***********************************
Estorno de transação.

Reverse
***********************************
A transação foi revertida. Isso acontece devido à alguma falha técnica em algum momento do fluxo.
Com isso todo o fluxo feito é revertido.
