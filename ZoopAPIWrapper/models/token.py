from ZoopAPIWrapper.models.base import ResourceModel


class Token(ResourceModel):
    """
    Token is a resource used to link a BankAccount Or Card and a Customer
    https://docs.zoop.co/reference#token-1

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        type: bank_account or card
        used: boolean of verification
    """
    RESOURCE = 'token'

    @classmethod
    def get_non_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = super().get_non_required_fields()
        return fields.union(
            {'type', 'used'}
        )
