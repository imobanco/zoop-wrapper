from decouple import config  # type: ignore

"""Zoop auth key"""
ZOOP_KEY = config("ZOOP_KEY", default="")

"""Zoop market place ID"""
MARKETPLACE_ID = config("MARKETPLACE_ID", default="")
