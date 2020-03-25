import logging


# noinspection PyPep8Naming
class classproperty(object):
    """
    Classproperty utils
    """
    def __init__(self, getter):
        """
        Initialize classproperty
        Args:
            getter: the method decorated
        """
        self.getter = getter

    def __get__(self, instance, owner):
        """
        get method of classproperty
        Args:
            instance: the instance owner
            owner: the class owner
        Returns:
        """
        return self.getter(owner)


def config_logging(log_level):
    """
    configure logging
    Args:
        log_level: log level to be notified
    """
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=log_level
    )


def get_logger(name):
    """
    Logger factory
    Args:
        name: subname to generate logger

    Returns: a new logger for ZoopAPIWrapper.{name}
    """
    return logging.getLogger(f'ZoopAPIWrapper.{name}')
