# -*- coding: utf-8 -*-

"""
etg.models
~~~~~~~~~~
This module contains the primary objects.
"""

from .exceptions import (
    ETGException, AuthErrorException, BadRequestException
)


class Response:
    __attrs__ = [
        'data', 'debug', 'error', 'status',
    ]

    def __init__(self, **kwargs):
        #: Main content of the response.
        self.data = kwargs.pop('data')

        #: Additional content of the response.
        # Contains initial requests parameters in json format and/or HTTP status.
        self.debug = kwargs.pop('debug')

        #: Error description.
        self.error = kwargs.pop('error')

        #: Response status code.
        self.status = kwargs.pop('status')

    @property
    def ok(self):
        """Returns True if there is no error in the response."""
        return self.status == 'ok'

    def raise_for_error(self):
        """Raises stored :class:`ETGException`, if one occurred."""
        if self.ok:
            return

        if self.error in ('incorrect_credentials', 'no_auth_header', 'invalid_auth_header'):
            raise AuthErrorException(self.error)
        elif self.error == 'invalid_params':
            error_msg = self.error
            if self.debug is not None and self.debug.get('validation_error') is not None:
                error_msg = ": ".join([error_msg, self.debug.get('validation_error')])
            raise BadRequestException(error_msg)
        else:
            raise ETGException(self.error)

    def __bool__(self):
        """Returns True if there is no error in the response."""
        return self.ok


class GuestData:
    def __init__(self, adults, children=None):
        """Init.

        :param adults: number of adult guests.
        :type adults: int
        :param children: (optional) age of children who will stay in the room.
        :type children: list[int] or None
        """
        self.adults = adults
        self.children = children if children is not None else []

    def to_json(self):
        return {
            'adults': self.adults,
            'children': self.children,
        }
