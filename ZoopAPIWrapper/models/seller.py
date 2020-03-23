from ZoopAPIWrapper.models.base import ZoopBase, ZoopMarketPlaceModel, Address


class Seller(ZoopMarketPlaceModel):
    RESOURCE = 'seller'

    __FIELDS = ["status", "type", "account_balance", "current_balance",
                "description", "statement_descriptor", "mcc",
                "show_profile_online", "is_mobile",
                "decline_on_fail_security_code",
                "decline_on_fail_zipcode",
                "delinquent", "payment_methods", "default_debit",
                "default_credit", "merchant_code", "terminal_code"]

    def __init__(self, status, type, account_balance, current_balance,
                 description, statement_descriptor, mcc, show_profile_online,
                 is_mobile, decline_on_fail_security_code,
                 decline_on_fail_zipcode, delinquent, payment_methods,
                 default_debit, default_credit, merchant_code, terminal_code,
                 **kwargs):
        super().__init__(**kwargs)

        self.status = status
        self.type = type
        self.account_balance = account_balance
        self.current_balance = current_balance
        self.description = description
        self.statement_descriptor = statement_descriptor
        self.mcc = mcc
        self.show_profile_online = show_profile_online
        self.is_mobile = is_mobile
        self.decline_on_fail_security_code = decline_on_fail_security_code
        self.decline_on_fail_zipcode = decline_on_fail_zipcode
        self.delinquent = delinquent
        self.payment_methods = payment_methods
        self.default_debit = default_debit
        self.default_credit = default_credit
        self.merchant_code = merchant_code
        self.terminal_code = terminal_code

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)

    @staticmethod
    def get_seller_class(_type):
        if _type == 'individual':
            return IndividualSeller
        elif _type == 'business':
            return BusinessSeller
        else:
            raise ValueError('seller type não identificado')

    @classmethod
    def from_dict(cls, data):
        _type = data.get('type')
        klass = Seller.get_seller_class(_type)
        return klass.from_dict(data)


class Owner(ZoopBase):
    __FIELDS = ["first_name", "last_name", "email",
                "taxpayer_id", "phone_number",
                "birthdate", "address"]

    def __init__(self, first_name, last_name, email,
                 taxpayer_id, phone_number, birthdate,
                 address, **kwargs):
        super().__init__(**kwargs)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.taxpayer_id = taxpayer_id
        self.phone_number = phone_number
        self.birthdate = birthdate
        self.address = Address.from_dict(address)

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class IndividualSeller(Seller, Owner):
    __FIELDS = ["website", "facebook", "twitter"]

    def __init__(self, website, facebook,
                 twitter, **kwargs):
        super().__init__(**kwargs)

        self.website = website
        self.facebook = facebook
        self.twitter = twitter

    @classmethod
    def from_dict(cls, data):
        return cls._from_dict(**data)

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class BusinessSeller(Seller):
    __FIELDS = ["business_name", "business_phone",
                "business_email", "business_website",
                "business_description", "business_opening_date",
                "business_facebook", "business_twitter", "ein",
                "owner", "business_address"]

    def __init__(self, business_name, business_phone,
                 business_email, business_website,
                 business_description, business_opening_date,
                 business_facebook, business_twitter, ein,
                 owner, business_address, **kwargs):
        super().__init__(**kwargs)

        self.business_name = business_name
        self.business_phone = business_phone
        self.business_email = business_email
        self.business_website = business_website
        self.business_description = business_description
        self.business_opening_date = business_opening_date
        self.business_facebook = business_facebook
        self.business_twitter = business_twitter
        self.ein = ein
        self.business_address = Address.from_dict(business_address)
        self.owner = Owner.from_dict(owner)

    @classmethod
    def from_dict(cls, data):
        return cls._from_dict(**data)

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)
