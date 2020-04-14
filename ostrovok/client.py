# -*- coding: utf-8 -*-
import json
import datetime

import requests
from requests.auth import HTTPBasicAuth

from .models import Response

HOST = 'https://partner.ostrovok.ru'
API_PATH = '/api/b2b/v2'


class OstrovokClient:
    def __init__(self, auth, verify_ssl=True):
        """Client for Ostrovok.ru Partners API v.2.

        API Documentation: https://partner.ostrovok.ru/wiki

        :param auth: Ostrovok user (key_id) and password (key) for basic auth.
        :type auth: (str, str)
        :param verify_ssl: (optional) controls whether we verify the server's SSL certificate, defaults to True.
        :type verify_ssl: bool
        """
        self.auth = HTTPBasicAuth(*auth)
        self.verify_ssl = verify_ssl

        self.req = None
        self.resp = None

    def request(self, method, resource, data=None):
        """Constructs and sends a request to Ostrovok API Gateway.

        :param method: HTTP method, possible values: ``GET``, or ``POST``.
        :type method: str
        :param resource: Ostrovok API resource.
        :type resource: str
        :param data: (optional) dictionary of parameters to send in the query string as the value of ``data``,
            e.g. data={'limit': 2, 'last_id': 123}, query string will be ``resource?data={"limit": 2, "last_id": 123}``.
        :type data: dict or None
        :return: Ostrovok API response/result, JSON document.
        :rtype: object
        """
        self.req = self.resp = None

        url = HOST + API_PATH + resource
        r = requests.request(method, url,
                             params=None if data is None else {'data': json.dumps(data)},
                             auth=self.auth, verify=self.verify_ssl)
        self.resp = Response(**r.json())

        self.resp.raise_for_error()

        return self.resp.result

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
