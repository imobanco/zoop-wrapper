import logging

from zoop_wrapper.exceptions import FieldError


def get_logger(name):
    """
    factory de Logger's

    Args:
        name: nome para gerar o logger

    Returns:
        novo logger para zoop_wrapper.{name}
    """
    return logging.getLogger(f"zoop_wrapper.{name}")


def convert_currency_float_value_to_cents(value):

    try:
        float(value)
    except (ValueError, TypeError) as e:
        raise FieldError(value, 'O input é inválido') from e

    try:
        int(value)
    except ValueError as e:
        raise FieldError(value, 'O input é inválido') from e

    value = int(float(value) * 100)

    return value
