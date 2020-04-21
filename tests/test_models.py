# -*- coding: utf-8 -*-
import pytest

from etg import Response
from etg.exceptions import (
    ETGException, BadRequestException, AuthErrorException
)

from .utils import load_response


class TestResponse:
    @pytest.mark.parametrize(
        'exception, fn', (
            (AuthErrorException, 'error_incorrect_credentials.json'),
            (AuthErrorException, 'error_invalid_auth_header.json'),
            (AuthErrorException, 'error_no_auth_header.json'),
            (BadRequestException, 'error_invalid_params.json'),
            (ETGException, 'error_decoding_json.json'),
            (ETGException, 'error_endpoint_exceeded_limit.json'),
            (ETGException, 'error_unknown.json'),
        ))
    def test_raise_for_error(self, exception, fn):
        with pytest.raises(exception) as exinfo:
            resp = Response(**load_response(fn))
            resp.raise_for_error()
        print(str(exinfo.value))
