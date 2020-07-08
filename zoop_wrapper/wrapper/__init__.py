from .bank_account import BankAccountWrapper
from .buyer import BuyerWrapper
from .card import CardWrapper
from .invoice import InvoiceWrapper
from .seller import SellerWrapper
from .transaction import TransactionWrapper
from .webhook import WebhookWrapper


class ZoopWrapper(
    BankAccountWrapper,
    BuyerWrapper,
    CardWrapper,
    InvoiceWrapper,
    SellerWrapper,
    TransactionWrapper,
    WebhookWrapper,
):
    """
    Zoop Wrapper

    It contains methods for all resources.
    """
