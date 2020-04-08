from zoop_wrapper.models.bank_account import BankAccount
from zoop_wrapper.models.buyer import Buyer
from zoop_wrapper.models.card import Card
from zoop_wrapper.models.invoice import Invoice
from zoop_wrapper.models.seller import Seller
from zoop_wrapper.models.token import Token
from zoop_wrapper.models.transaction import Transaction
from zoop_wrapper.utils import get_logger


logger = get_logger('models')


RESOURCE_CLASSES = [
    BankAccount, Buyer, Card, Invoice, Seller, Token, Transaction]
RESOURCES_DICT = {CLASS.RESOURCE: CLASS for CLASS in RESOURCE_CLASSES}


def _get_model_class_from_resource(resource):
    """
    getter for model from resource

    Examples:
        >>> _get_model_class_from_resource('seller')
        Seller
        >>> _get_model_class_from_resource('bank_account')
        BankAccount

    Args:
        resource: string of resource

    Raises:
        ValueError: when the resource is not identified

    Returns: ZoopModel subclass
    """
    if resource in RESOURCES_DICT:
        return RESOURCES_DICT.get(resource)

    raise ValueError(f'model não identificado para resource {resource}!')


def get_instance_from_data(data):
    """
    getter for model from resource.
    Factory Pattern

    Examples:
        >>> data = {'resource': 'seller'}
        >>> get_instance_from_data(data)
        Seller.from_dict(data)
        >>> data = {'resource': 'bank_account'}
        >>> get_instance_from_data(data)
        BankAccount.from_dict(data)

    Args:
        data: dict of data

    Returns: ZoopModel subclass instance or None
    """
    resource = data.get('resource')

    try:
        klass = _get_model_class_from_resource(resource)
        return klass.from_dict(data, allow_empty=True)
    except ValueError as e:
        logger.info(e)
        return None
