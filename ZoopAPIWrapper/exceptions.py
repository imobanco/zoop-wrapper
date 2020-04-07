class ValidationError(Exception):
    """
    Exception for when a validation occur for
    some ZoopObject.
    """
    def __init__(self, entity, errors):
        self.class_name = entity.__class__.__name__

        if isinstance(errors, list):
            self.errors = errors
        else:
            self.errors = [errors]

        super().__init__(
            f'Validation failed for {self.class_name}! '
            f'Missing fields: {self.errors}'
        )
