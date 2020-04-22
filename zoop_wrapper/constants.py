from decouple import config  # type: ignore


ZOOP_KEY = config("ZOOP_KEY", default="")
"""Chave de autenticação da Zoop"""


MARKETPLACE_ID = config("MARKETPLACE_ID", default="")
"""Marketplace id da Zoop"""
