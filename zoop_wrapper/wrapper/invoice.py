from .base import BaseZoopWrapper


class InvoiceWrapper(BaseZoopWrapper):
    """
    Possui os métodos do resource for :class:`.Invoice`
    """

    def retrieve_invoice(self, identifier):
        """
        Pega um :class:`.Invoice`

        Args:
            identifier: uuid id

        Returns:
            resposta com instância do :class:`.Invoice`
        """
        url = self._construct_url(action="boletos", identifier=identifier)
        return self._get(url)
