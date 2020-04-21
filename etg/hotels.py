# -*- coding: utf-8 -*-
import datetime

from .client import ETGClient


class ETGHotelsClient(ETGClient):
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
        :param guests: list of guests in the rooms, e.g. [{'adults': 2, 'children': []}].
            The max number of rooms in one request is 6.
        :type guests: list
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
        api_endpoint = ''
        data = dict()
        if isinstance(ids, list):
            api_endpoint = 'api/b2b/v3/search/serp/hotels/'
            data['ids'] = ids
        elif isinstance(ids, int):
            api_endpoint = 'api/b2b/v3/search/serp/region/'
            data['region_id'] = ids
        data.update({
            'checkin': checkin.strftime('%Y-%m-%d'),
            'checkout': checkout.strftime('%Y-%m-%d'),
            'guests': guests,
        })
        if currency is not None:
            data['currency'] = currency
        if residency is not None:
            data['residency'] = residency
        if timeout is not None:
            data['timeout'] = timeout
        if upsells is not None:
            data['upsells'] = upsells
        if language is not None:
            data['language'] = language
        response = self.request('POST', api_endpoint, data=data)

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
        :param guests: list of guests in the rooms, e.g. [{'adults': 2, 'children': []}].
            The max number of rooms in one request is 6.
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
        :param guests: list of guests in the rooms, e.g. [{'adults': 2, 'children': []}].
            The max number of rooms in one request is 6.
        :param kwargs: optional parameters.
            For more information, see the description of ``self.search`` method.
        :return: list of available hotels (Region Search Engine Results Page).
        :rtype: list
        """
        return self.search(region_id, checkin, checkout, guests, **kwargs)

    def hotel_rates(self, ids, checkin, checkout):
        """Searches hotels with available accommodation that meets the given search conditions.

        It is not recommended to let the users choose the rates from this method.

        :param ids: list of hotels identifiers or region identifier.
        :type ids: list[str] or int
        :param checkin: check-in date, no later than 366 days from today.
        :type checkin: datetime.date
        :param checkout: check-out date, no later than 30 days from check-in date.
        :type checkout: datetime.date
        :return: list of available hotels.
        :rtype: list
        """
        data = dict()
        if isinstance(ids, list):
            data['ids'] = ids
        elif isinstance(ids, int):
            data['region_id'] = ids
        data['checkin'] = checkin.strftime('%Y-%m-%d')
        data['checkout'] = checkout.strftime('%Y-%m-%d')

        response = self.request('GET', '/hotel/rates', data=data)

        hotels = list()
        if isinstance(response, dict):
            hotels = response.get('hotels')

        return hotels

    def hotelpage(self, hotel_id, checkin, checkout,
                  adults=2, children=None, currency='default'):
        """Returns actual rates for the given hotel.

        This request is necessary to make a booking via API.
        Value of `book_hash` in results of this API method can be passed as `book_hash` when sending booking requests.

        :param hotel_id: hotel identifier.
        :type hotel_id: str
        :param checkin: check-in date, no later than 366 days from today.
        :type checkin: datetime.date
        :param checkout: check-out date, no later than 30 days from check-in date.
        :type checkout: datetime.date
        :param adults: number of adult guests, min number: 1, max number: 6.
        :type adults: int
        :param children: age of children who will stay in the room, max age - 17, max number - 4, e.g. [0,4,9].
        :type children: list or None
        :param currency: currency code of the rooms` rate in the response, e.g. 'USD', 'EUR', 'RUB' or 'default'.
        :type currency: str
        :return: hotel info with actual available rates.
        :rtype: dict or None
        """
        data = {
            'checkin': checkin.strftime('%Y-%m-%d'),
            'checkout': checkout.strftime('%Y-%m-%d'),
            'adults': adults,
            'children': [] if children is None else children,
            'currency': currency,
        }
        result = self.request('GET', '/hotelpage/' + hotel_id, data=data)

        hotel = None
        if isinstance(result, dict) and isinstance(result.get('hotels'), list) and len(result.get('hotels')):
            hotel = result.get('hotels')[0]

        return hotel

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

        regions = self.request('GET', '/region/list', data=data)

        return regions
