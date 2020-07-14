Transação de Cartão de crédito
========================================

No mundo de transações de cartão de crédito, existem os eventos::


    - pre autorização
    - captura


Pré autorização
***********************************
A pré autorização realiza o bloqueio do valor no cartão de crédito do comprador.

.. important::
    Mas isso não realiza o pagamento, vulgo débito do valor!


Captura
***********************************
A captura realiza o pagamento propriamente dito do valor passado!

.. important::
    O valor passado pode ser menor ou igual ao valor pré autorizado. Nesse cenário a diferença é desbloqueada automaticamente para o comprador.

.. warning::
    Se o valor desejado a ser capturado for maior do que o valor pré autorizado, a transação deverá ser estornada e feita novamente.
