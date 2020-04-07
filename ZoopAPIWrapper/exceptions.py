class FieldError(Exception):
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason
        super().__init__(self.to_dict())

    def to_dict(self):
        return {self.name: self.reason}


class ValidationError(Exception):
    """
    Exception for when a validation occur for
    some ZoopObject.
    """
    def __init__(self, entity, errors):
        if type(entity) == type:
            self.class_name = entity.__name__
        else:
            self.class_name = type(entity).__name__

        if isinstance(errors, list):
            self.errors = errors
        else:
            self.errors = [errors]

        super().__init__(
            f'Validation failed for {self.class_name}! '
            f'Errors: {self.parse_errors()}'
        )

    def parse_errors(self):
        errors_list = []
        for error in self.errors:
            if isinstance(error, FieldError):
                errors_list.append(error.to_dict())
            else:
                errors_list.append(error)
        return errors_list
