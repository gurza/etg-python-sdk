# -*- coding: utf-8 -*-
import os
import datetime
import time
import uuid

import pytest

from etg import ETGHotelsClient
from etg import (  # models
    GuestData,
)
from etg import ETGException

auth = (os.getenv('ETG_KEY_ID'), os.getenv('ETG_KEY'))
partner_email = os.getenv('ETG_MAIL')
client = ETGHotelsClient(auth)


class TestResources:
    hotel_id = 'test_hotel'
    region_id = 6308866  # region with test hotel id (Белогорск, Амурская область)
    checkin = datetime.date.today() + datetime.timedelta(days=60)
    checkout = checkin + datetime.timedelta(days=5)
    guests = [GuestData(2)]

    def test_autocomplete(self):
        language = 'en'
        response = client.autocomplete('Berlin', language=language)
        assert len(response.get('hotels', [])) > 0
        assert len(response.get('regions', [])) > 0

    @pytest.mark.parametrize(
        'adults, children', (
            (2, []),
            (2, [1]),
        ))
    def test_search(self, adults, children):
        ids = [self.hotel_id]
        guests = [GuestData(adults, children)]
        currency = 'EUR'
        residency = 'gb'
        language = 'en'
        available_hotels = client.search(ids, self.checkin, self.checkout, guests,
                                         currency=currency, residency=residency, language=language)

        debug_request = dict()
        if isinstance(client.resp.debug, dict) and client.resp.debug.get('request') is not None:
            debug_request = client.resp.debug.get('request')

        # rates in response
        assert len(available_hotels[0].get('rates')) > 0

        # check search conditions
        assert debug_request.get('ids') == ids

        assert debug_request.get('checkin') == self.checkin.strftime('%Y-%m-%d')
        assert debug_request.get('checkout') == self.checkout.strftime('%Y-%m-%d')
        assert all(map(lambda rate: len(rate.get('daily_prices', [])) == (self.checkout - self.checkin).days,
                       available_hotels[0].get('rates')))

        assert len(debug_request.get('guests')) == len(guests)
        assert debug_request.get('guests')[0].get('adults') == adults
        assert debug_request.get('guests')[0].get('children') == children

        assert debug_request.get('currency') == currency
        assert all(map(
            lambda rate: rate.get('payment_options').get('payment_types')[0].get('show_currency_code') == currency,
            available_hotels[0].get('rates')))

        assert debug_request.get('residency') == residency

        assert debug_request.get('language') == language

    def test_search_by_hotels(self):
        ids = [self.hotel_id]
        available_hotels = client.search_by_hotels(ids, self.checkin, self.checkout, self.guests)
        assert len(available_hotels[0].get('rates')) > 0

    def test_search_by_region(self):
        available_hotels = client.search_by_region(self.region_id, self.checkin, self.checkout, self.guests)
        assert len(available_hotels[0].get('rates')) > 0

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


class OrderValuesStorage:
    partner_order_id = None
    book_hash = None
    payment_amount = None


@pytest.mark.incremental
class TestMainFlow:
    partner_order_id = str(uuid.uuid4())
    language = 'ru'
    currency = 'RUB'
    payment_type = 'deposit'
    hotel_id = 'test_hotel'
    checkin = datetime.date.today() + datetime.timedelta(days=60)
    checkout = checkin + datetime.timedelta(days=5)
    guests = [GuestData(2)]
    rooms = [
        {
            'guests': [
                {
                    'first_name': 'Anna',
                    'last_name': 'Ostrovok',
                },
                {
                    'first_name': 'Marta',
                    'last_name': 'Ostrovok',
                },
            ],
        },
    ]

    def test_hotelpage(self):
        hotel = client.hotelpage(self.hotel_id, self.checkin, self.checkout, self.guests,
                                 currency=self.currency, language=self.language)
        acceptable_rates = list(
            filter(lambda r: r.get('payment_options').get('payment_types')[0].get('type') == self.payment_type,
                   hotel.get('rates'))
        )
        assert len(acceptable_rates) > 0
        OrderValuesStorage.book_hash = acceptable_rates[0].get('book_hash')

    def test_make_reservation(self):
        book_hash = OrderValuesStorage.book_hash
        fake_user_ip = '8.8.8.8'
        reservation = client.make_reservation(self.partner_order_id, book_hash, self.language, fake_user_ip)
        assert reservation is not None
        acceptable_payment_types = list(
            filter(lambda pt: pt.get('type') == self.payment_type and pt.get('currency_code') == self.currency,
                   reservation.get('payment_types', []))
        )
        assert len(acceptable_payment_types) > 0
        OrderValuesStorage.payment_amount = acceptable_payment_types[0].get('amount')

    def test_finish_reservation(self):
        partner = {
            'partner_order_id': self.partner_order_id,
        }
        payment_type = {
            'type': self.payment_type,
            'amount': OrderValuesStorage.payment_amount,
            'currency_code': self.currency,
        }
        rooms = self.rooms
        user = {
            'email': partner_email,
            'phone': '01122333',
        }
        language = self.language
        is_completed = client.finish_reservation(partner, payment_type, rooms, user, language)
        assert is_completed
        OrderValuesStorage.partner_order_id = self.partner_order_id
        print('partner_order_id:', self.partner_order_id)

    def test_get_voucher(self):
        language = self.language
        voucher = client.get_voucher(OrderValuesStorage.partner_order_id, language)
        assert voucher

    def test_cancel(self):
        is_canceled = False
        for i in range(5):
            time.sleep(5)
            try:
                is_canceled = client.cancel(self.partner_order_id)
            except ETGException:
                continue
            break

        assert is_canceled
