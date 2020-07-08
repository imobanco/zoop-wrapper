from .bank_account import BankAccount
from .buyer import Buyer
from .card import Card
from .invoice import Invoice
from .seller import Seller
from .token import Token
from .transaction import Transaction
from .webhook import Webhook
from ..utils import get_logger


logger = get_logger("models")


RESOURCE_CLASSES = [
    BankAccount,
    Buyer,
    Card,
    Invoice,
    Seller,
    Token,
    Transaction,
    Webhook,
]
RESOURCES_DICT = {CLASS.RESOURCE: CLASS for CLASS in RESOURCE_CLASSES}


def _get_model_class_from_resource(resource):
    """
    Get ``model class`` from ``resource``

    Examples:
        >>> _get_model_class_from_resource('seller')
        Seller
        >>> _get_model_class_from_resource('bank_account')
        BankAccount

    Args:
        resource (str): value of resource

    Raises:
        ValueError: when the ``resource`` is not identified

    Returns:
            :class:`.ResourceModel` subclass
    """
    if resource in RESOURCES_DICT:
        return RESOURCES_DICT.get(resource)

    raise ValueError(f"model não identificado para resource {resource}!")


def get_instance_from_data(data):
    """
    ``Factory Pattern`` for :class:`.ResourceModel` subclasses

    Examples:
        >>> data = {'resource': 'seller'}
        >>> get_instance_from_data(data)
        Seller.from_dict(data)
        >>> data = {'resource': 'bank_account'}
        >>> get_instance_from_data(data)
        BankAccount.from_dict(data)

    Args:
        data (dict): data

    Returns:
            :class:`.ResourceModel` subclass or ``None``
    """
    resource = data.get("resource")

    try:
        klass = _get_model_class_from_resource(resource)
        return klass.from_dict(data, allow_empty=True)
    except ValueError as e:
        logger.info(e)
        return None
