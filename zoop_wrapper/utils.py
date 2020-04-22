import logging


def config_logging():
    """
    configura o formato de log
    """
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def get_logger(name):
    """
    factory de Logger's

    Args:
        name: nome para gerar o logger

    Returns:
        novo logger para zoop_wrapper.{name}
    """
    return logging.getLogger(f"zoop_wrapper.{name}")
