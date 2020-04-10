# -*- coding: utf-8 -*-
import os

import pytest

from ostrovok import OstrovokClient
from ostrovok.exceptions import (
    OstrovokException, BadRequest, AuthError
)

from .utils import load_response

auth = (os.getenv('OSTROVOK_KEY_ID'), os.getenv('OSTROVOK_KEY'))
client = OstrovokClient(auth)


class TestBasic:
    def test_client_create(self):
        assert client is not None

    @pytest.mark.parametrize(
        'exception, fn', (
            (AuthError, 'auth_failed.json'),
            (BadRequest, 'validation_invalid_params.json'),
            (OstrovokException, 'too_many_requests.json'),
            (OstrovokException, 'unexpected_error.json'),
        ))
    def test_errors(self, exception, fn):
        with pytest.raises(exception):
            client.resp = load_response(fn)
            client.raise_for_error()


class TestInfoResources:
    def test_region_list(self):
        regions = client.region_list()
        last_id = regions[-1].get('id')
        regions_count = len(regions)
        assert regions_count > 0

        # check ``last_id`` parameter
        regions_filtered_by_last_id = client.region_list(last_id=last_id)
        assert len(regions_filtered_by_last_id) > 0
        assert all(map(lambda region: region.get('id') > last_id, regions_filtered_by_last_id))

        # check ``limit`` parameter
        limit = regions_count // 2
        assert len(client.region_list(limit=limit)) == limit

        # check ``types`` parameter
        types = ['Country', 'Province (State)']
        regions_filtered_by_types = client.region_list(types=types)
        assert any(map(lambda region: region.get('type') == types[0], regions_filtered_by_types))
        assert any(map(lambda region: region.get('type') == types[1], regions_filtered_by_types))
