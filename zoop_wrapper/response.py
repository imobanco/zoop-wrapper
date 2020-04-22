from requests.models import Response


class ZoopResponse(Response):
    """
    Uma :class:`.Response` recebida da API da Zoop.

    Attributes:
        data (dict): json da resposta
        instance (:class:`.ResourceModel`): instância do recurso
        instances (list of :class:`.ResourceModel`): lista de instâncias do recurso
    """
