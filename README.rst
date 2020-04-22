.. |br| raw:: html

  <br/>

|br|

.. image:: https://zoop.com.br/wp-content/themes/zoop/img/logo.svg
   :target: https://zoop.com.br/wp-content/themes/zoop/img/logo.svg
   :alt: Zoop Logo
   :height: 100px
   :align: center

|br| |br|

.. container::

    .. image:: https://img.shields.io/pypi/v/zoop-wrapper
       :target: https://pypi.org/project/zoop-wrapper/
       :alt: PyPI Version
    .. image:: https://img.shields.io/pypi/pyversions/zoop-wrapper
       :target: https://pypi.org/project/zoop-wrapper/
       :alt: PyPI - Python Version

.. container::

    .. image:: https://img.shields.io/github/workflow/status/imobanco/zoop-wrapper/tests
       :target: https://github.com/imobanco/zoop-wrapper/actions?query=workflow%3Atests
       :alt: Test status
    .. image:: https://img.shields.io/github/license/imobanco/zoop-wrapper
       :target: https://github.com/imobanco/zoop-wrapper/blob/dev/LICENSE
       :alt: Licença
    .. image:: https://img.shields.io/github/contributors/imobanco/zoop-wrapper
       :target: https://github.com/imobanco/zoop-wrapper/graphs/contributors
       :alt: Contributors

.. container::

    .. image:: https://api.codacy.com/project/badge/Grade/d78080aeddcc411696a91bb18f9fe953
       :target: https://www.codacy.com/gh/imobanco/zoop-wrapper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=imobanco/zoop-wrapper&amp;utm_campaign=Badge_Grade
       :alt: Code grade
    .. image:: https://api.codacy.com/project/badge/Coverage/d78080aeddcc411696a91bb18f9fe953
       :target: https://www.codacy.com/gh/imobanco/zoop-wrapper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=imobanco/zoop-wrapper&amp;utm_campaign=Badge_Coverage
       :alt: Coverage
    .. image:: https://snyk.io/test/github/imobanco/zoop-wrapper/badge.svg?targetFile=requirements.txt
       :target: https://snyk.io/test/github/imobanco/zoop-wrapper?targetFile=requirements.txt
       :alt: Known Vulnerabilities

==================
Introdução
==================
Cliente não oficial da Zoop feito em Python, para realizar integração com o gateway de pagamento.
`Documentação oficial da Zoop <https://docs.zoop.co>`__


Configuração
==================
Para utilizar o `zoop-wrapper` é necessário ter duas constantes/variáveis. sendo elas:

.. code-block:: python

    ZOOP_KEY='chave de autenticação recebida da zoop'
    MARKETPLACE_ID='ID do market place'

Recomendamos criar um arquivo `.env` contendo essas varíaveis de ambiente.

Podem ser criadas diretamente no terminal utilizando (não recomendado):

.. code-block:: bash

    export ZOOP_KEY='chave de autenticação recebida da zoop'
    export MARKETPLACE_ID='ID do market place'


Podem ser criadas também diretamente no `arquivo.py`

.. danger::

    Fazer isso além de não ser recomendado é uma **FALHA** de segurança.

Modo de usar
==================
Na `pasta de exemplos <examples/>`__ existem alguns demostrativos.

Documentação da Zoop
=====================
A Zoop fornece diversas formas de comunicação. Sendo uma telas API's baseadas na tecnologia REST. 
A documentação da API da zoop não é uma das melhores, mas está disponível abertamente.

.. warning::

    Não tenho conhecimento se TODOS testes podem ser realizados testes sem ônus ao desenvolvedor.

    As transações de cartão podem ser extornadas e não há problema em gerar boletos (não paga a baixa).

Saiba mais na `documentação oficial da Zoop <https://docs.zoop.co/docs/introdu%C3%A7%C3%A3o-a-zoop>`__

Recursos disponíveis
=====================

.. list-table:: Market Place
   :align: center

   * - função
   * - Albatross
   * - Crunchy Frog
   * - Gannet Ripple



Market Place
=============
<details>
<summary>Market place</summary>

- [ ] detalhes
</details>

<details>
<summary>webhooks</summary>

- [ ] Cadastro
- [ ] listagem
- [ ] detalhes
- [ ] remoção
</details>

<details>
<summary>Buyer</summary>

- [x] Cadastro
- [x] listagem
- [x] detalhes
- [x] remoção
</details>

<details>
<summary>Seller</summary>

- [x] Cadastro
- [x] listagem
- [x] detalhes
- [x] remoção
</details>

<details>
<summary>Token</summary>

- [x] Cadastro de token cartão de crédito
- [x] Cadastro de token conta bancária
- [ ] detalhes
</details>

<details>
<summary>Cartão de crédito</summary>

- [x] Conexão
- [x] detalhes
- [ ] remoção
</details>

<details>
<summary>Conta bancária</summary>

- [x] Conexão
- [x] listagem
- [x] detalhes
- [ ] remoção
</details>

<details>
<summary>Boleto</summary>

- [x] detalhes
</details>

<details>
<summary>Transação</summary>

- [x] listagem
- [x] detalhes
- [x] cancelamento
- [x] Cadastro transação boleto
- [ ] Cadastro transação cartão de crédito
</details>
