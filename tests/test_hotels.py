# -*- coding: utf-8 -*-
import os
import datetime

import pytest

from etg import ETGHotelsClient

auth = (os.getenv('ETG_KEY_ID'), os.getenv('ETG_KEY'))
client = ETGHotelsClient(auth)


class TestResources:
    ids = ['test_hotel']
    region_id = 6308866  # region with test hotel id (Белогорск, Амурская область)
    checkin = datetime.date.today() + datetime.timedelta(days=60)
    checkout = checkin + datetime.timedelta(days=5)
    guests = [{
        'adults': 2,
        'children': [],
    }]

    @pytest.mark.parametrize(
        'adults, children', (
            (2, []),
            (2, [6]),
        ))
    def test_search(self, adults, children):
        guests = [{
            'adults': adults,
            'children': children,
        }]
        currency = 'EUR'
        residency = 'gb'
        language = 'en'
        available_hotels = client.search(self.ids, self.checkin, self.checkout, guests,
                                         currency=currency, residency=residency, language=language)

        debug_request = dict()
        if isinstance(client.resp.debug, dict) and client.resp.debug.get('request') is not None:
            debug_request = client.resp.debug.get('request')

        # rates in response
        assert len(available_hotels[0].get('rates')) > 0

        # check search conditions
        assert debug_request.get('ids') == self.ids

        assert debug_request.get('checkin') == self.checkin.strftime('%Y-%m-%d')
        assert debug_request.get('checkout') == self.checkout.strftime('%Y-%m-%d')
        assert all(map(lambda rate: len(rate.get('daily_prices', [])) == (self.checkout - self.checkin).days,
                       available_hotels[0].get('rates')))

        assert len(debug_request.get('guests')) == len(guests)
        assert debug_request.get('guests')[0].get('adults') == guests[0].get('adults')
        assert debug_request.get('guests')[0].get('children') == guests[0].get('children')

        assert debug_request.get('currency') == currency
        assert all(map(
            lambda rate: rate.get('payment_options').get('payment_types')[0].get('show_currency_code') == currency,
            available_hotels[0].get('rates')))

        assert debug_request.get('residency') == residency

        assert debug_request.get('language') == language

    def test_search_by_hotels(self):
        available_hotels = client.search_by_hotels(self.ids, self.checkin, self.checkout, self.guests)
        assert len(available_hotels[0].get('rates')) > 0

    def test_search_by_region(self):
        available_hotels = client.search_by_region(self.region_id, self.checkin, self.checkout, self.guests)
        assert len(available_hotels[0].get('rates')) > 0

    def test_hotelpage(self):
        checkin = datetime.date.today() + datetime.timedelta(days=60)
        checkout = checkin + datetime.timedelta(days=5)
        assert client.hotelpage('test_hotel', checkin, checkout) is not None

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
