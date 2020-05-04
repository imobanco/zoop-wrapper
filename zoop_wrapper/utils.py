import logging


def get_logger(name):
    """
    factory de Logger's

    Args:
        name: nome para gerar o logger

    Returns:
        novo logger para zoop_wrapper.{name}
    """
    return logging.getLogger(f"zoop_wrapper.{name}")
