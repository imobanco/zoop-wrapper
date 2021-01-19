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
    """
    Converte o valor recebido (que pode ser str<int>, int, float, str<float>)
    para um inteiro em centavos.

    Essa função trunca a terceira casa decimal em diante de um float.

    Examples:
        1234 => 1234
        56.78 => 5678
        56.78123 => 5678
        56.7 => 5670
        653.55 => 65355
        "9876" => 9876
        "91.23" => 9123

    Args:
        value: Valor a ser convertido

    Returns:
        número inteiro em centavos
    """
    try:
        float(value)
    except (ValueError, TypeError) as e:
        raise FieldError(value, "O input é inválido") from e

    string_value = str(value)

    if "." in string_value:
        split_value = string_value.split(".")
        int_value = split_value[0]
        float_value = split_value[1]
        float_value = float_value.ljust(2, "0")
        value = f"{int_value}{float_value[:2]}"

    return int(value)
