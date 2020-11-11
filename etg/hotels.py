# -*- coding: utf-8 -*-
import datetime

from .client import ETGClient
from .models import (
    GuestData,
)


class ETGHotelsClient(ETGClient):
    def autocomplete(self, query,
                     language=None):
        """Finds regions and hotels by a part of their names.

        :param query: part of hotel or region name.
        :type query: str
        :param language: (optional) language of the response, e.g. 'en', 'ru'.
        :type language: str
        :return: suggested hotels and regions, no more than 5 objects for each category.
        :rtype: dict
        """
        endpoint = 'api/b2b/v3/search/multicomplete/'
        data = {
            'query': query,
            'language': language,
        }
        response = self.request('POST', endpoint, data=data)
        return response

    def search(self, ids, checkin, checkout, guests,
               currency=None, residency=None, timeout=None, upsells=None,
               language=None):
        """Searches hotels with available accommodation that meets the given conditions.

        It is not recommended to let the users choose the rates from this method response.

        :param ids: list of hotels identifiers or region identifier.
        :type ids: list[str] or int
        :param checkin: check-in date, no later than 366 days from today.
        :type checkin: datetime.date
        :param checkout: check-out date, no later than 30 days from check-in date.
        :type checkout: datetime.date
        :param guests: list of guests in the rooms.
            The max number of rooms in one request is 6.
        :type guests: list[GuestData]
        :param currency: (optional) currency code of the rooms rate in the response, e.g. 'GBP', 'USD', 'RUB'.
            Default value is contract currency.
        :type currency: str or None
        :param residency: (optional) guest's (or multiple guests') nationality.
            Use it in case there are doubts regarding country/hotel policy towards citizens of a specific country.
            Value format is specified by standard 'ISO 3166-1 alpha-2', e.g. 'gb', 'us', 'ru'.
        :type residency: str or None
        :param timeout: (optional) response timeout in seconds.
        :type timeout: int or None
        :param upsells: (optional) additional services request.
        :type upsells: dict or None
        :param language: (optional) language of static information in the response, e.g. 'en', 'ru'.
            Default value is contract language.
        :type language: str or None
        :return: list of available hotels.
        :rtype: list
        """
        endpoint = None
        if isinstance(ids, list):
            endpoint = 'api/b2b/v3/search/serp/hotels/'
        elif isinstance(ids, int):
            endpoint = 'api/b2b/v3/search/serp/region/'
        data = {
            'ids': ids,
            'region_id': ids,
            'checkin': checkin.strftime('%Y-%m-%d'),
            'checkout': checkout.strftime('%Y-%m-%d'),
            'guests': guests,
            'currency': currency,
            'residency': residency,
            'timeout': timeout,
            'upsells': upsells if upsells is not None else {},
            'language': language,
        }
        response = self.request('POST', endpoint, data=data)

        hotels = list()
        if isinstance(response, dict):
            hotels = response.get('hotels')

        return hotels

    def search_by_hotels(self, ids, checkin, checkout, guests, **kwargs):
        """Searches hotels with available accommodation that meets the given conditions.

        :param ids: list of hotels identifiers.
        :type ids: list[str]
        :param checkin: check-in date, no later than 366 days from today.
        :type checkin: datetime.date
        :param checkout: check-out date, no later than 30 days from check-in date.
        :type checkout: datetime.date
        :param guests: list of guests in the rooms.
            The max number of rooms in one request is 6.
        :type guests: list[GuestData]
        :param kwargs: optional parameters.
            For more information, see the description of ``self.search`` method.
        :return: list of available hotels (Hotels Search Engine Results Page).
        :rtype: list
        """
        return self.search(ids, checkin, checkout, guests, **kwargs)

    def search_by_region(self, region_id, checkin, checkout, guests, **kwargs):
        """Searches hotels with available accommodation that meets the given conditions.

        :param region_id: region identifier.
        :type region_id: int
        :param checkin: check-in date, no later than 366 days from today.
        :type checkin: datetime.date
        :param checkout: check-out date, no later than 30 days from check-in date.
        :type checkout: datetime.date
        :param guests: list of guests in the rooms.
            The max number of rooms in one request is 6.
        :type guests: list[GuestData]
        :param kwargs: optional parameters.
            For more information, see the description of ``self.search`` method.
        :return: list of available hotels (Region Search Engine Results Page).
        :rtype: list
        """
        return self.search(region_id, checkin, checkout, guests, **kwargs)

    def hotelpage(self, hotel_id, checkin, checkout, guests,
                  currency=None, residency=None, upsells=None, language=None):
        """Returns actual rates for the given hotel.

        This request is necessary to make a booking via API.
        Value of `book_hash` in results of this API method can be passed as `book_hash` when sending booking requests.

        :param hotel_id: hotel identifier.
        :type hotel_id: str
        :param checkin: check-in date, no later than 366 days from today.
        :type checkin: datetime.date
        :param checkout: check-out date, no later than 30 days from check-in date.
        :type checkout: datetime.date
        :param guests: list of guests in the rooms.
            The max number of rooms in one request is 6.
        :type guests: list[GuestData]
        :param currency: (optional) currency code of the rooms rate in the response, e.g. 'GBP', 'USD', 'RUB'.
            Default value is contract currency.
        :type currency: str or None
        :param residency: (optional) guest's (or multiple guests') nationality.
            Use it in case there are doubts regarding country/hotel policy towards citizens of a specific country.
            Value format is specified by standard 'ISO 3166-1 alpha-2', e.g. 'gb', 'us', 'ru'.
        :type residency: str or None
        :param timeout: (optional) response timeout in seconds.
        :type timeout: int or None
        :param upsells: (optional) additional services request.
        :type upsells: dict or None
        :param language: (optional) language of static information in the response, e.g. 'en', 'ru'.
            Default value is contract language.
        :type language: str or None
        :return: hotel info with actual available rates.
        :rtype: dict or None
        """
        endpoint = 'api/b2b/v3/search/hp/'
        data = {
            'id': hotel_id,
            'checkin': checkin.strftime('%Y-%m-%d'),
            'checkout': checkout.strftime('%Y-%m-%d'),
            'guests': guests,
            'currency': currency,
            'residency': residency,
            'upsells': upsells if upsells is not None else {},
            'language': language,
        }
        response = self.request('POST', endpoint, data=data)

        hotel = None
        if isinstance(response, dict) and isinstance(response.get('hotels'), list) and len(response.get('hotels')):
            hotel = response.get('hotels')[0]

        return hotel

    def make_reservation(self, partner_order_id, book_hash, language, user_ip):
        """Makes a new reservation.

        :param partner_order_id: unique order id on partner side, e.g. '0a0f4e6d-b337-43be-a5f8-484492ebe033'.
        :type partner_order_id: str
        :param book_hash: unique identifier of the rate from hotelpage response.
        :type book_hash: str
        :param language: language of the reservation, e.g. 'en', 'ru'.
        :type language: str
        :param user_ip: customer IP address, e.g. '8.8.8.8'.
        :type user_ip: str
        :return: reservation info.
        :rtype: dict
        """
        endpoint = 'api/b2b/v3/hotel/order/booking/form/'
        data = {
            'partner_order_id': partner_order_id,
            'book_hash': book_hash,
            'language': language,
            'user_ip': user_ip,
        }
        response = self.request('POST', endpoint, data=data)

        return response

    def finish_reservation(self, partner, payment_type, rooms, user, language,
                           arrival_datetime=None, upsell_data=None, return_path=None):
        """Completes the reservation.

        :param partner: partner information.
            partner_order_id: partner order id.
            comment: (optional) partner booking inner comment. It is visible only to the partner himself.
            amount_sell_b2b2c: (optional) reselling price for the client in contract currency.
        :type partner: dict
        :param payment_type: payment information.
            type: payment type option, possible values: 'now', 'hotel', 'deposit'.
            amount: amount of the order.
            currency_code: ISO currency code, e.g. 'EUR'.
            init_uuid: (optional) token of the booking payment operation.
            pay_uuid: (optional) token of the booking payment check.
        :type payment_type: dict
        :param rooms: guest data by the rooms.
        :type rooms: list
        :param user: guest additional information.
            email: partner manager email.
            phone: guest telephone number.
            comment: (optional) guest comment sent to the hotel.
        :type user: dict
        :param language: language of the reservation, e.g. 'en', 'ru'.
        :type language: str
        :param arrival_datetime: (optional) estimated arrival time to the hotel.
        :type arrival_datetime: datetime.datetime
        :param upsell_data: (optional) upsell information.
        :type upsell_data: list or None
        :param return_path: (optional) URL on the partner side to which the user will be forwarded
            by the payment gateway after 3D Secure verification.
        :type return_path: str
        :return: True if the reservation is completed.
        :rtype: bool
        """
        endpoint = 'api/b2b/v3/hotel/order/booking/finish/'
        data = {
            'partner': partner,
            'payment_type': payment_type,
            'rooms': rooms,
            'user': user,
            'language': language,
            'arrival_datetime': arrival_datetime,
            'upsell_data': upsell_data if upsell_data is not None else [],
            'return_path': return_path,
        }
        self.request('POST', endpoint, data=data)
        return True

    def cancel(self, partner_order_id):
        """Cancels reservation.

        :param partner_order_id: partner order id, e.g. '0a0f4e6d-b337-43be-a5f8-484492ebe033'.
        :type partner_order_id: str
        :return: True if the reservation is canceled.
        :rtype: bool
        """
        endpoint = 'api/b2b/v3/hotel/order/cancel/'
        data = {
            'partner_order_id': partner_order_id,
        }
        self.request('POST', endpoint, data=data)
        return True

    def region_list(self, last_id=None, limit=None, types=None):
        """Returns information about regions.

        :param last_id: (optional) all retrieved regions will have an ID that exceeds the given value.
        :type last_id: int or None
        :param limit: (optional) maximum number of regions in a response, cannot exceed 10000, default value = 1000.
        :type limit: int or None
        :param types: (optional) condition for filtering regions by region type, possible values:
            ``Airport``, ``Bus Station``, ``City``, ``Continent``, ``Country``,
            ``Multi-City (Vicinity)``, ``Multi-Region (within a country)``, ``Neighborhood``,
            ``Point of Interest``, ``Province (State)``,``Railway Station``, ``Street``,
            ``Subway (Entrace)``.
        :type types: list[str] or None
        :return: returns information about regions.
        :rtype: list
        """
        data = dict()
        if last_id is not None:
            data['last_id'] = last_id
        if limit is not None:
            data['limit'] = limit
        if types is not None:
            data['types'] = types

        regions = self.request('GET', 'region/list', data=data)

        return regions

    def get_voucher(self, partner_order_id, language):
        data = {
            'partner_order_id': partner_order_id,
            'language': language,
        }

        voucher = self.request('GET', 'hotel/order/document/voucher/download/', data=data, stream=True)

        return voucher
