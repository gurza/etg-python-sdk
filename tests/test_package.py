# -*- coding: utf-8 -*-
import pytest

from ostrovok import OstrovokClient


class TestPackage:
    def test_client_create(self):
        client = OstrovokClient()
        assert client is not None
