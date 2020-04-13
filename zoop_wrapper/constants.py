from decouple import config  # type: ignore

"""Zoop auth key"""
ZOOP_KEY = config("ZOOP_KEY", default="")

"""Zoop market place ID"""
MARKETPLACE_ID = config("MARKETPLACE_ID", default="")

"""Log level for lib logging"""
LOG_LEVEL = config("LOG_LEVEL", cast=int, default=30)
