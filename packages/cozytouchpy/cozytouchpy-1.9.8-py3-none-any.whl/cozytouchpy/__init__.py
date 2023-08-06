# -*- coding:utf-8 -*-
"""Provides authentification and row access to Cozytouch modules."""
from .client import CozytouchClient
from .exception import AuthentificationFailed, CozytouchException, HttpRequestFailed

name = "cozytouchpy"
__version__ = "1.9.8"
__all__ = [
    "CozytouchClient",
    "AuthentificationFailed",
    "CozytouchException",
    "HttpRequestFailed",
]
