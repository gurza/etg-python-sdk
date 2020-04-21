# -*- coding: utf-8 -*-

"""
etg.exceptions
~~~~~~~~~~~~~~

This module contains the set of exceptions.
"""


class ETGException(IOError):
    """There was an ambiguous exception that occurred while handling your request."""


class BadRequestException(ETGException, ValueError):
    """Request GET or POST data does not validate."""


class AuthErrorException(ETGException, ValueError):
    """Authentication failed."""
