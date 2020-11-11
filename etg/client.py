# -*- coding: utf-8 -*-
import json

import requests
from requests.auth import HTTPBasicAuth

from .models import Response


class ETGClient:

    """
    Client for ETG API v3 (general API resources).
    """
    API_HOST = 'https://api.worldota.net/api/b2b/v3'
    SUPPORTED_LANGUAGES = (
        'bg', 'de', 'el', 'en', 'es', 'fr', 'it',
        'hu', 'pl', 'pt', 'ro', 'ru', 'sr', 'tr',
    )

    def __init__(self, auth, verify_ssl=True):
        """Init.

        :param auth: user (key_id) and password (key) for basic auth.
        :type auth: (str, str)
        :param verify_ssl: (optional) controls whether we verify the server's SSL certificate, defaults to True.
        :type verify_ssl: bool
        """
        self.auth = HTTPBasicAuth(*auth)
        self.verify_ssl = verify_ssl

        self.req = None
        self.resp = None

    def request(self, method, endpoint,
                data=None, stream=False):
        """Constructs and sends a request to API Gateway.

        :param method: HTTP method, possible values: ``GET``, or ``POST``.
        :type method: str
        :param endpoint: API endpoint, e.g. 'api/b2b/v3/general/financial/info/',
            find list of available endpoints at https://api.worldota.net/api/b2b/v3/overview/.
        :type endpoint: str
        :param data: (optional) dictionary of parameters to send in the query string as the value of ``data``,
            e.g. data={'limit': 2, 'last_id': 123}, query string will be ``resource?data={"limit": 2, "last_id": 123}``.
        :type data: dict or None
        :param stream: Set True to download binary response.
        :type stream: bool
        :return: main content of the response API (`$.data`).
        :rtype: object
        """
        self.req = self.resp = None

        r_params = r_data = None
        if data is not None:
            if method == 'GET':
                r_params = {'data': json.dumps(data, cls=MultiJSONEncoder)}
            elif method == 'POST':
                r_data = json.dumps(data, cls=MultiJSONEncoder)

        url = '{api_host}/{endpoint}'.format(api_host=self.API_HOST, endpoint=endpoint)
        r = requests.request(method, url,
                             params=r_params, data=r_data, auth=self.auth, verify=self.verify_ssl,
                             stream=False)

        if stream:
            r.raise_for_status()
            return r.content

        self.resp = Response(**r.json())

        self.resp.raise_for_error()

        return self.resp.data

    def contract_data_info(self):
        """Returns contracts general information.

        :return: info for all own contracts.
        :rtype: dict
        """
        endpoint = 'api/b2b/v3/general/contract/data/info/'
        response_data = self.request('GET', endpoint)
        return response_data

    def financial_info(self):
        """Returns contracts financial information.

        :return: financial info for all own contracts.
        :rtype: dict
        """
        endpoint = 'api/b2b/v3/general/financial/info/'
        response_data = self.request('GET', endpoint)
        return response_data


class MultiJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json') and callable(o.to_json):
            return o.to_json()
        # Let the base class default raise the TypeError
        return json.JSONEncoder.default(self, o)
