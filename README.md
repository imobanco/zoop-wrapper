<br/>

<div align="center">
	<img height="200" src="https://zoop.com.br/wp-content/themes/zoop/img/logo.svg" alt="Zoop">

[![tests](https://img.shields.io/github/workflow/status/imobanco/zoop-wrapper/tests)](https://github.com/imobanco/zoop-wrapper/actions?query=workflow%3Atests)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d78080aeddcc411696a91bb18f9fe953)](https://www.codacy.com/gh/imobanco/zoop-wrapper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=imobanco/zoop-wrapper&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/d78080aeddcc411696a91bb18f9fe953)](https://www.codacy.com/gh/imobanco/zoop-wrapper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=imobanco/zoop-wrapper&amp;utm_campaign=Badge_Coverage)

[![PyPI](https://img.shields.io/pypi/v/zoop-wrapper)](https://pypi.org/project/zoop-wrapper/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zoop-wrapper)](https://pypi.org/project/zoop-wrapper/)

[![GitHub](https://img.shields.io/github/license/imobanco/zoop-wrapper)](https://github.com/imobanco/zoop-wrapper/blob/dev/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/imobanco/zoop-wrapper)](https://github.com/imobanco/zoop-wrapper/graphs/contributors)
[![Known Vulnerabilities](https://snyk.io/test/github/imobanco/zoop-wrapper/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/imobanco/zoop-wrapper?targetFile=requirements.txt)

<br/>

</div>

<br/>

# Introdução
Cliente não oficial da Zoop feito em Python, para realizar integração com o gateway de pagamento.

[Documentação oficial da Zoop](https://docs.zoop.co/).

## Configuração
Para utilizar o `zoop-wrapper` é necessário ter duas constantes/variáveis. sendo elas:
```python
ZOOP_KEY='chave de autenticação recebida da zoop'
MARKETPLACE_ID='ID do market place'
```

Recomendamos criar um arquivo `.env` contendo essas varíaveis de ambiente. 

Podem ser criadas diretamente no terminal utilizando (não recomendado):
```shell script
export ZOOP_KEY='chave de autenticação recebida da zoop'
export MARKETPLACE_ID='ID do market place'
```

Podem ser criadas diretamente no `arquivo.py`, porém fazer isso além de ser não recomendado é uma **FALHA** 
de segurança.

## Modo de usar
Na [pasta de exemplos](examples/) existem alguns demostrativos.

## Documentação da Zoop
A Zoop fornece diversas formas de comunicação. Sendo uma telas API's baseadas na tecnologia REST. 
A documentação da API da zoop não é uma das melhores, mas está disponível abertamente.

>Atenção: Não tenho conhecimento se TODOS testes podem ser realizados testes sem ônus ao desenvolvedor. 
>As transações de cartão podem ser extornadas e não há problema em gerar boletos (não paga a baixa).

Saiba mais na [documentação oficial da Zoop](https://docs.zoop.co/docs/introdu%C3%A7%C3%A3o-a-zoop)

## Recursos disponíveis

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
