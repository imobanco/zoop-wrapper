![alt text](https://zoop.com.br/wp-content/themes/zoop/img/logo.svg "Zoop")

[![tests](https://img.shields.io/github/workflow/status/imobanco/ZoopAPIWrapper/Python%20application%20tests)](https://github.com/imobanco/ZoopAPIWrapper/actions)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d78080aeddcc411696a91bb18f9fe953)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=imobanco/ZoopAPIWrapper&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/d78080aeddcc411696a91bb18f9fe953)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=imobanco/ZoopAPIWrapper&utm_campaign=Badge_Coverage)

![PyPI](https://img.shields.io/pypi/v/zoop-wrapper)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zoop-wrapper)

![GitHub](https://img.shields.io/github/license/imobanco/ZoopAPIWrapper)
![GitHub contributors](https://img.shields.io/github/contributors/imobanco/ZoopAPIWrapper)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/imobanco/ZoopAPIWrapper)

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
