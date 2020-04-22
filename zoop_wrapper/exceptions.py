class FieldError(Exception):
    """
    Exceção para ser usada quando a validação de algum campo falha.
    """

    def __init__(self, name, reason):
        """
        Args:
            name: nome do campo
            reason: motivo do erro
        """
        self.name = name
        self.reason = reason
        super().__init__(self.to_dict())

    def to_dict(self):
        """
        transforma exceção para um dict

        Returns:
            dict
        """
        return {self.name: self.reason}


class ValidationError(Exception):
    """
    Exceção para ser usada quando a validação de um ZoopObject ocorre
    """

    def __init__(self, entity, errors):
        """
        Args:
            entity: entidade na qual o erro ocorreu
            errors: lista de qualquer coisa (preferencialmente :class:`.FieldError`)
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
            f"Validação falhou para {self.class_name}! " f"Erros: {self.parse_errors()}"
        )

    def parse_errors(self):
        """
        Traduz os erros do tipo :class:`.FieldError` para dict na listagem de erros

        Returns: lista de objetos serializáveis
        """
        errors_list = []
        for error in self.errors:
            if isinstance(error, FieldError):
                errors_list.append(error.to_dict())
            else:
                errors_list.append(error)
        return errors_list
