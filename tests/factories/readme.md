# Módulo Factories
Essa magia toda tem várias etapas/partes

## Faker
Ele gera atributos randomicos dos [providers](https://faker.readthedocs.io/en/latest/providers.html)

## Factory
O Factory que é um Factory Pattern.

1.  [Aqui o Factory configura o `model_class` pegando do `Meta`](https://github.com/FactoryBoy/factory_boy/blob/a8da29e21b42544fe208b8f641836ca2f2b222c2/factory/base.py#L207)
2.  [Aqui se tem a instanciação do objeto. É chamado o método `_create` de acordo com a estratégia.](https://github.com/FactoryBoy/factory_boy/blob/a8da29e21b42544fe208b8f641836ca2f2b222c2/factory/base.py#L310)
3.  [Esse `instantiate` já recebe todos os attributos configurados com o Faker como `*args` ou `**kwargs`. E o Builder que faz essa mágica.](https://github.com/FactoryBoy/factory_boy/blob/a8da29e21b42544fe208b8f641836ca2f2b222c2/factory/builder.py#L270)
