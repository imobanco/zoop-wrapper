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

    __FIELDS = ["holder_name", "taxpayer_id", "description",
                "bank_name", "bank_code", "type",
                "last4_digits", "account_number",
                "country_code", "routing_number",
                "phone_number", "is_active", "is_verified",
                "debitable", "customer", "fingerprint",
                "address", "verification_checklist"]

    def __init__(self, holder_name, taxpayer_id, description,
                 bank_name, bank_code, type, account_number,
                 country_code, routing_number,
                 phone_number, is_active, is_verified,
                 debitable, customer, fingerprint,
                 address, verification_checklist, last4_digits=None, **kwargs):
        super().__init__(**kwargs)

        self.holder_name = holder_name
        self.taxpayer_id = taxpayer_id
        self.description = description
        self.bank_name = bank_name
        self.bank_code = bank_code
        self.type = type
        self.last4_digits = last4_digits
        self.account_number = account_number
        self.country_code = country_code
        self.routing_number = routing_number
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
