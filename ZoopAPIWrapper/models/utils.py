from ZoopAPIWrapper.models.seller import Seller
from ZoopAPIWrapper.models.bank_account import BankAccount


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
    if resource == Seller.RESOURCE:
        return Seller
    elif resource == BankAccount.RESOURCE:
        return BankAccount
    else:
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
        return klass.from_dict(data)
    except ValueError as e:
        print(e)
        return None
