from ZoopAPIWrapper.models.seller import Seller
from ZoopAPIWrapper.models.bank_account import BankAccount
from ZoopAPIWrapper.models.token import Token


RESOURCE_CLASSES = [BankAccount, Seller, Token]
RESOURCES_DICT = {CLASS.RESOURCE: CLASS for CLASS in RESOURCE_CLASSES}


def _get_model_class_from_resource(resource):
    if resource in RESOURCES_DICT:
        return RESOURCES_DICT.get(resource)

    raise ValueError(f'model não identificado para resource {resource}!')


def get_instance_from_data(data):
    resource = data.get('resource')

    try:
        klass = _get_model_class_from_resource(resource)
        return klass.from_dict(data)
    except ValueError as e:
        print(e)
        return None
