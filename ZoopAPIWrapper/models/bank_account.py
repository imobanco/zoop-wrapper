from ZoopAPIWrapper.models.base import ZoopBase, ZoopModel, Address


class VerificationChecklist(ZoopBase):
    __FIELDS = ["postal_code_check", "address_line1_check",
                "deposit_check"]

    def __init__(self, postal_code_check, address_line1_check,
                 deposit_check, **kwargs):
        super().__init__(**kwargs)

        self.postal_code_check = postal_code_check
        self.address_line1_check = address_line1_check
        self.deposit_check = deposit_check

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class BankAccount(ZoopModel):
    RESOURCE = 'bank_account'

    __FIELDS = ["holder_name", "description",
                "bank_name", "bank_code", "type",
                "last4_digits", "account_number",
                "country_code", "routing_number",
                "phone_number", "is_active", "is_verified",
                "debitable", "customer", "fingerprint",
                "address", "verification_checklist"]

    def __init__(self, holder_name, bank_code, routing_number,
                 account_number,
                 description=None, bank_name=None, type=None,
                 country_code=None, phone_number=None,
                 is_active=None, is_verified=None,
                 debitable=None, customer=None, fingerprint=None,
                 address=None, verification_checklist=None, last4_digits=None, **kwargs):
        super().__init__(**kwargs)

        self.holder_name = holder_name
        self.bank_code = bank_code
        self.routing_number = routing_number
        self.account_number = account_number

        self.description = description
        self.bank_name = bank_name
        self.type = type
        self.last4_digits = last4_digits
        self.country_code = country_code
        self.phone_number = phone_number
        self.is_active = is_active
        self.is_verified = is_verified
        self.debitable = debitable
        self.customer = customer
        self.fingerprint = fingerprint
        self.address = Address.from_dict(address)
        self.verification_checklist = VerificationChecklist\
            .from_dict(verification_checklist)

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)

    @staticmethod
    def get_bank_account_class(customer_identifier_type):
        if customer_identifier_type == 'taxpayer_id':
            return IndividualBankAccount
        elif customer_identifier_type == 'ein':
            return BusinessBankAccount
        else:
            raise ValueError('costumer_identifier type não identificado')

    @classmethod
    def from_dict(cls, data):
        taxpayer_id = data.get('taxpayer_id')
        ein = data.get('ein')
        if taxpayer_id is None and ein is None:
            raise TypeError('missing customer_identifier. Must be "taxpayer_id" or "ein"')
        elif taxpayer_id is not None:
            customer_identifier_type = 'taxpayer_id'
        else:
            customer_identifier_type = 'ein'

        klass = BankAccount.get_bank_account_class(customer_identifier_type)
        return klass.from_dict(data)


class BusinessBankAccount(BankAccount):
    __FIELDS = ["ein"]

    def __init__(self, ein, **kwargs):
        super().__init__(**kwargs)

        self.ein = ein

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)

    @classmethod
    def from_dict(cls, data):
        return cls._from_dict(**data)


class IndividualBankAccount(BankAccount):
    __FIELDS = ["taxpayer_id"]

    def __init__(self, taxpayer_id, **kwargs):
        super().__init__(**kwargs)

        self.taxpayer_id = taxpayer_id

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)

    @classmethod
    def from_dict(cls, data):
        return cls._from_dict(**data)
