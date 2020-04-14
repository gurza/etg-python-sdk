# -*- coding: utf-8 -*-

"""
ostrovok.models
~~~~~~~~~~~~~~~
This module contains the primary objects.
"""

from .exceptions import (
    OstrovokException, AuthErrorException, BadRequestException
)


class Response:
    def __init__(self, **kwargs):
        self.debug = kwargs.pop('debug')
        self.result = kwargs.pop('result')
        self.error = kwargs.pop('error')

    @property
    def success(self):
        """Returns True if there is no error in the response."""
        return self.error is None

    def raise_for_error(self):
        """Raises stored :class:`OstrovokException`, if one occurred."""
        if self.success:
            return

        slug = self.error.get('slug')
        extra = self.error.get('extra')
        error_msg = self.error.get('description')
        if slug == 'auth_failed':
            if extra is not None and len(extra.get('errors')):
                extra_msg = '. '.join([msg for msg in extra.get('errors')])
                error_msg = '. '.join([error_msg, extra_msg])
            raise AuthErrorException(error_msg)
        elif slug == 'validation_invalid_params':
            if extra is not None and len(extra.get('validation_errors')):
                extra_msg = ', '.join([err.get('field') + ': ' + err.get('error', [])[0]
                                       for err in extra.get('validation_errors')])
                error_msg = '. '.join([error_msg, extra_msg])
            raise BadRequestException(error_msg)
        else:
            raise OstrovokException(error_msg)

    def __bool__(self):
        """Returns True if there is no error in the response."""
        return self.success
