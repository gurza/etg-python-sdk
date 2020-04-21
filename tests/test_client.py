# -*- coding: utf-8 -*-
import os

import pytest

from etg import ETGClient
from etg import ETGException

auth = (os.getenv('ETG_KEY_ID'), os.getenv('ETG_KEY'))
client = ETGClient(auth)


class TestBasic:
    def test_client_create(self):
        assert client is not None

    def test_api_access(self):
        try:
            client.financial_info()
        except ETGException as ex:
            pytest.fail('API error: {0}'.format(ex))


class TestResources:
    def test_contract_data_info(self):
        contracts = client.contract_data_info().get('contract_datas', [])
        assert len(contracts) > 0

    def test_financial_info(self):
        contracts = client.financial_info().get('contract_datas', [])
        assert len(contracts)
