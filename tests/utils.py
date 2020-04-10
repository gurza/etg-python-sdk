# -*- coding: utf-8 -*-
import os
import json

here = os.path.abspath(os.path.dirname(__file__))


def load_response(resp_fn):
    """Returns a json response from the given file."""
    with open(os.path.join(here, 'test_api_responses', resp_fn), encoding='utf-8') as f:
        resp = json.loads(f.read())
    return resp
