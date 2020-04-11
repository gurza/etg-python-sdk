# -*- coding: utf-8 -*-
import os
import datetime

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


class TestResources:
    @pytest.mark.parametrize(
        'ids, cnt', (
            (['000'], 0),  # fare hotel
            (['test_hotel'], 1),  # test hotel
            (['000', 'test_hotel'], 1),
            (6308866, 1),  # region with test hotel id (Белогорск, Амурская область)
        ))
    def test_hotel_rate(self, ids, cnt):
        checkin = datetime.date.today() + datetime.timedelta(days=60)
        checkout = checkin + datetime.timedelta(days=5)
        availability_response = client.hotel_rates(ids, checkin, checkout)

        # check ``checkin`` and ``checkout`` parameters
        debug_returns = isinstance(client.resp, dict) and isinstance(client.resp.get('debug'), dict)
        assert debug_returns
        if debug_returns:
            assert client.resp.get('debug').get('checkin') == checkin.strftime('%Y-%m-%d')
            assert client.resp.get('debug').get('checkout') == checkout.strftime('%Y-%m-%d')

        # check result
        assert len(availability_response) == cnt

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
