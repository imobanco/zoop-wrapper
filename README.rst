.. |br| raw:: html

  <br/>

|br|

.. image:: https://zoop.com.br/wp-content/themes/zoop/img/logo.svg
   :target: #
   :alt: Zoop Logo
   :height: 130
   :align: center

|br|

.. container::

    .. image:: https://img.shields.io/pypi/v/zoop-wrapper
       :target: https://pypi.org/project/zoop-wrapper/
       :alt: PyPI Version
       :height: 23
    .. image:: https://img.shields.io/pypi/pyversions/zoop-wrapper
       :target: https://pypi.org/project/zoop-wrapper/
       :alt: PyPI - Python Version
       :height: 23

.. container::

    .. image:: https://img.shields.io/github/workflow/status/imobanco/zoop-wrapper/tests
       :target: https://github.com/imobanco/zoop-wrapper/actions?query=workflow%3Atests
       :alt: Test status
       :height: 23
    .. image:: https://readthedocs.org/projects/zoop-wrapper/badge/?version=latest
       :target: https://zoop-wrapper.readthedocs.io/pt_BR/latest/?badge=latest
       :alt: Documentation Status
       :height: 23

.. container::

    .. image:: https://img.shields.io/github/license/imobanco/zoop-wrapper
       :target: https://github.com/imobanco/zoop-wrapper/blob/dev/LICENSE
       :alt: Licença
       :height: 23
    .. image:: https://img.shields.io/github/contributors/imobanco/zoop-wrapper
       :target: https://github.com/imobanco/zoop-wrapper/graphs/contributors
       :alt: Contributors
       :height: 23

.. container::

    .. image:: https://codecov.io/gh/imobanco/zoop-wrapper/branch/master/graph/badge.svg
       :target: https://codecov.io/gh/imobanco/zoop-wrapper
       :alt: Coverage
       :height: 21
    .. image:: https://snyk.io/test/github/imobanco/zoop-wrapper/badge.svg?targetFile=requirements.txt
       :target: https://snyk.io/test/github/imobanco/zoop-wrapper?targetFile=requirements.txt
       :alt: Known Vulnerabilities
       :height: 23

|br|

Cliente não oficial da Zoop feito em Python, para realizar integração com o gateway de pagamento.

`Documentação oficial da Zoop <https://docs.zoop.co>`_


Instalando
===========

Nosso pacote está hospedado no `PyPI <https://pypi.org/project/zoop-wrapper/>`_

.. code-block:: bash

    pip install zoop-wrapper


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

Documentação da Zoop
=====================
A Zoop fornece diversas formas de comunicação. Sendo uma telas API's baseadas na tecnologia REST. 
A documentação da API da zoop não é uma das melhores, mas está disponível abertamente.

.. warning::

    Não temos conhecimento se TODOS os testes podem ser realizados sem ônus ao desenvolvedor.

    As transações de cartão podem ser extornadas e não há problema em gerar boletos (não paga a baixa).

Saiba mais na `documentação oficial da Zoop <https://docs.zoop.co/docs/introdu%C3%A7%C3%A3o-a-zoop>`_

Recursos disponíveis
=====================

Market Place

- ☐ detalhes


Webhooks

- ☑ Cadastro
- ☑ listagem
- ☑ detalhes
- ☑ remoção


Buyer

- ☑ Atualização
- ☑ Cadastro
- ☑ listagem
- ☑ detalhes
- ☑ remoção


Seller

- ☑ Atualização
- ☑ Cadastro
- ☑ listagem
- ☑ detalhes
- ☑ remoção


Token

- ☑ Cadastro de token cartão de crédito
- ☑ Cadastro de token conta bancária
- ☐ detalhes


Cartão de crédito

- ☑ Conexão
- ☑ detalhes
- ☐ remoção


Conta bancária

- ☐ Atualização
- ☑ Conexão
- ☑ listagem
- ☑ detalhes
- ☐ remoção


Boleto

- ☑ detalhes


Transação

- ☑ listagem
- ☑ detalhes
- ☑ cancelamento
- ☑ Cadastro transação boleto
- ☑ Cadastro transação cartão de crédito

