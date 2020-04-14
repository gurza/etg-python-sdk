# -*- coding: utf-8 -*-

"""
ostrovok.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of exceptions.
"""


class OstrovokException(IOError):
    """There was an ambiguous exception that occurred while handling your request."""


class BadRequestException(OstrovokException, ValueError):
    """Request GET or POST data does not validate."""


class AuthErrorException(OstrovokException, ValueError):
    """Authentication failed."""
