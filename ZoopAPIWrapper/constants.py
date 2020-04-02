from decouple import config


ZOOP_KEY = config('ZOOP_KEY')
MARKETPLACE_ID = config('MARKETPLACE_ID')

LOG_LEVEL = config('LOG_LEVEL', cast=int)
