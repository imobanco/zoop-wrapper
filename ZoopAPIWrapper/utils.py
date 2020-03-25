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
            getter:
        """
        self.getter = getter

    def __get__(self, instance, owner):
        """
        get method of classproperty
        Args:
            instance:
            owner:
        Returns:
        """
        return self.getter(owner)


def config_logging(log_level):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=log_level
    )


def get_logger(name):
    return logging.getLogger(f'ZoopAPIWrapper.{name}')
