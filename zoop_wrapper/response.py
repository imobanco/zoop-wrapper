from requests.models import Response


class ZoopResponse(Response):
    """
    Uma :class:`requests.Response` recebida da API da Zoop.

    .. danger:: Essa classe NÃO é utilizada no código (não é instanciada).

        Está na biblioteca apenas para ter o type hinting.
        Esses atributos são adicionados ao objeto :class:`requests.Response`

    Attributes:
        data (dict): json da resposta
    """
