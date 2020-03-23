from ZoopAPIWrapper.models.seller import Seller
from ZoopAPIWrapper.models.bank_account import BankAccount


def _get_model_class_from_resource(resource):
    if resource == Seller.RESOURCE:
        return Seller
    if resource == BankAccount.RESOURCE:
        return Seller
    else:
        raise ValueError(f'model não identificado para resource {resource}!')


def get_instance_from_data(data):
    resource = data.get('resource')

    try:
        klass = _get_model_class_from_resource(resource)
        return klass.from_dict(data)
    except ValueError:
        return None
