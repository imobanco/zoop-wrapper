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
