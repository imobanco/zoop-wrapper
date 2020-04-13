![alt text](https://zoop.com.br/wp-content/themes/zoop/img/logo.svg "Zoop")

[![tests](https://img.shields.io/github/workflow/status/imobanco/zoop-wrapper/Python%20application%20tests)](https://github.com/imobanco/zoop-wrapper/actions)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d78080aeddcc411696a91bb18f9fe953)](https://www.codacy.com/gh/imobanco/zoop-wrapper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=imobanco/zoop-wrapper&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/d78080aeddcc411696a91bb18f9fe953)](https://www.codacy.com/gh/imobanco/zoop-wrapper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=imobanco/zoop-wrapper&amp;utm_campaign=Badge_Coverage)

![PyPI](https://img.shields.io/pypi/v/zoop-wrapper)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zoop-wrapper)

![GitHub](https://img.shields.io/github/license/imobanco/zoop-wrapper)
![GitHub contributors](https://img.shields.io/github/contributors/imobanco/zoop-wrapper)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/imobanco/zoop-wrapper)

# Introdução
Cliente não oficial da Zoop feito em Python, para realizar integração com o gateway de pagamento.

[Documentação oficial da Zoop](https://docs.zoop.co/).

## Recursos disponíveis

### Market place
- [ ] detalhes

### webhooks
- [ ] Cadastro
- [ ] listagem
- [ ] detalhes
- [ ] remoção

### Buyer
- [x] Cadastro
- [x] listagem
- [x] detalhes
- [x] remoção

### Seller
- [x] Cadastro
- [x] listagem
- [x] detalhes
- [x] remoção

### Token
- [x] Cadastro de token cartão de crédito
- [x] Cadastro de token conta bancária
- [ ] detalhes

### Cartão de crédito
- [x] Conexão
- [x] detalhes
- [ ] remoção

### Conta bancária
- [x] Conexão
- [x] listagem
- [x] detalhes
- [ ] remoção

### Boleto
- [x] detalhes

### Transação
- [x] listagem
- [x] detalhes
- [x] cancelamento
- [x] Cadastro transação boleto
- [ ] Cadastro transação cartão de crédito

## Modo de usar
A Zoop fornece diversas formas de comunicação. Sendo uma telas API's baseadas na tecnologia REST.

A documentação da API da zoop não é uma das melhores, mas está disponível abertamente.

Atenção: Não tenho conhecimento se TODOS testes podem ser realizados testes sem ônus ao desenvolvedor. 
As transações de cartão podem ser extornadas e não há problema em gerar boletos (não paga a baixa).

Saiba mais na [documentação oficial da Zoop](https://docs.zoop.co/docs/introdu%C3%A7%C3%A3o-a-zoop)