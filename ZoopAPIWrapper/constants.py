from decouple import config  # type: ignore

"""Zoop auth key"""
ZOOP_KEY = config('ZOOP_KEY')

"""Zoop market place ID"""
MARKETPLACE_ID = config('MARKETPLACE_ID')

"""Log level for lib"""
LOG_LEVEL = config('LOG_LEVEL', cast=int)
