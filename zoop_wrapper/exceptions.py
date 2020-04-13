class FieldError(Exception):
    """
    Exception to be used when the validation
    of some field fail.
    """

    def __init__(self, name, reason):
        """
        Args:
            name: name of the field
            reason: string containing the reason of the fail
        """
        self.name = name
        self.reason = reason
        super().__init__(self.to_dict())

    def to_dict(self):
        """
        transform exception to dict

        Returns:
            dict
        """
        return {self.name: self.reason}


class ValidationError(Exception):
    """
    Exception to be used when the validation
    of some ZoopObject occur.
    """

    def __init__(self, entity, errors):
        """
        Args:
            entity: entity where the error occurred
            errors: list or anything
        """
        if type(entity) == type:
            self.class_name = entity.__name__
        else:
            self.class_name = type(entity).__name__

        if isinstance(errors, list):
            self.errors = errors
        else:
            self.errors = [errors]

        super().__init__(
            f"Validation failed for {self.class_name}! "
            f"Errors: {self.parse_errors()}"
        )

    def parse_errors(self):
        """
        Parse the list of errors to plain list of something
        Returns: list of something
        """
        errors_list = []
        for error in self.errors:
            if isinstance(error, FieldError):
                errors_list.append(error.to_dict())
            else:
                errors_list.append(error)
        return errors_list
