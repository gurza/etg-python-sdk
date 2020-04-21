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
        if isinstance(ids, list):
            api_endpoint = 'api/b2b/v3/search/serp/hotels/'
        elif isinstance(ids, int):
            api_endpoint = 'api/b2b/v3/search/serp/region/'
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
        :return: hotel info with actual available rates.
        :rtype: dict or None
        """
        api_endpoint = 'api/b2b/v3/search/hp/'
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
        response = self.request('POST', api_endpoint, data=data)

        hotel = None
        if isinstance(response, dict) and isinstance(response.get('hotels'), list) and len(response.get('hotels')):
            hotel = response.get('hotels')[0]

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
