import logging


def config_logging(log_level):
    """
    configure logging
    Args:
        log_level: log level to be notified
    """
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=log_level
    )


def get_logger(name):
    """
    Logger factory
    Args:
        name: subname to generate logger

    Returns:
        a new logger for zoop_wrapper.{name}
    """
    return logging.getLogger(f"zoop_wrapper.{name}")
