# -*- coding: utf-8 -*-

"""
ostrovok.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of exceptions.
"""


class OstrovokException(IOError):
    """There was an ambiguous exception that occurred while handling your request."""

    def __init__(self, *args, **kwargs):
        """Initialize OstrovokException with `request` and `response` fields."""
        self.response = kwargs.pop('response', None)
        self.request = kwargs.pop('request', None)
        super(OstrovokException, self).__init__(*args, **kwargs)


class BadRequest(OstrovokException, ValueError):
    """Request GET or POST data does not validate."""


class AuthError(OstrovokException, ValueError):
    """Authentication failed."""
