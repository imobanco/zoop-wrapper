from .bank_account import BankAccountWrapper
from .buyer import BuyerWrapper
from .card import CardWrapper
from .invoice import InvoiceWrapper
from .seller import SellerWrapper
from .transaction import TransactionWrapper
from .webhook import WebHookWrapper


class ZoopWrapper(
    BankAccountWrapper,
    BuyerWrapper,
    CardWrapper,
    InvoiceWrapper,
    SellerWrapper,
    TransactionWrapper,
    WebHookWrapper,
):
    """
    Zoop Wrapper

    It contains methods for all resources.
    """
