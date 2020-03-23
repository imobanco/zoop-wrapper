
class ZoopBase:
    __FIELDS = []

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def _from_dict(cls, **entries):
        return cls(**entries)

    @classmethod
    def from_dict(cls, data):
        return cls._from_dict(**data)

    def to_dict(self):
        data = {}
        for field in self.fields:
            try:
                data[field] = self.__getattribute__(field).to_dict()
            except AttributeError:
                data[field] = self.__getattribute__(field)
        return data

    @property
    def fields(self):
        return list(self.__FIELDS)


class ZoopModel(ZoopBase):
    __FIELDS = ["id", "resource", "uri", "created_at", "updated_at", "metadata"]

    def __init__(self, id, resource, uri, created_at, updated_at, metadata, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.resource = resource
        self.uri = uri

        self.created_at = created_at
        self.updated_at = updated_at
        self.metadata = metadata

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class ZoopMarketPlaceModel(ZoopModel):
    __FIELDS = ["marketplace_id"]

    def __init__(self, marketplace_id, **kwargs):
        super().__init__(**kwargs)

        self.marketplace_id = marketplace_id

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class Seller(ZoopMarketPlaceModel):
    RESOURCE = 'seller'

    __FIELDS = ["status", "type", "account_balance", "current_balance",
                "description", "statement_descriptor", "mcc", "show_profile_online",
                "is_mobile", "decline_on_fail_security_code", "decline_on_fail_zipcode",
                "delinquent", "payment_methods", "default_debit", "default_credit",
                "merchant_code", "terminal_code"]

    def __init__(self, status, type, account_balance, current_balance,
                 description, statement_descriptor, mcc, show_profile_online,
                 is_mobile, decline_on_fail_security_code, decline_on_fail_zipcode,
                 delinquent, payment_methods, default_debit, default_credit,
                 merchant_code, terminal_code, **kwargs):
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


class Address(ZoopBase):
    __FIELDS = ["line1", "line2", "line3",
                "neighborhood", "city", "state",
                "postal_code", "country_code"]

    def __init__(self, line1, line2, line3,
                 neighborhood, city, state,
                 postal_code, country_code, **kwargs):
        super().__init__(**kwargs)

        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country_code = country_code

    @property
    def fields(self):
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


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
