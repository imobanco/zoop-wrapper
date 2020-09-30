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

    try:
        if isinstance(value, float):
            raise ValueError(
                "O valor é um float. Então podemos fazer o tratamento dele!"
            )
        int(value)
    except ValueError:
        value = int(float(value) * 100)
    finally:
        value = int(value)

    return value
