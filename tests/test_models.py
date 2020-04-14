# -*- coding: utf-8 -*-
import pytest

from ostrovok import Response
from ostrovok.exceptions import (
    OstrovokException, BadRequestException, AuthErrorException
)

from .utils import load_response


class TestResponse:
    @pytest.mark.parametrize(
        'exception, fn', (
            (AuthErrorException, 'auth_failed.json'),
            (BadRequestException, 'validation_invalid_params.json'),
            (OstrovokException, 'too_many_requests.json'),
            (OstrovokException, 'unexpected_error.json'),
        ))
    def test_raise_for_error(self, exception, fn):
        with pytest.raises(exception):
            resp = Response(**load_response(fn))
            resp.raise_for_error()
