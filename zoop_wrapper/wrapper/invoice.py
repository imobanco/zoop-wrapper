from ..wrapper.base import BaseZoopWrapper


class InvoiceWrapper(BaseZoopWrapper):
    """
    Invoice Wrapper

    Contains methods for :class:`.Invoice` resource
    """

    def retrieve_invoice(self, identifier):
        """
        retrieve invoice

        Args:
            identifier: uuid id

        Returns:
            response with instance of Invoice
        """
        url = self._construct_url(action="boletos", identifier=identifier)
        return self._get(url)
