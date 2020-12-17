# -*- coding: utf-8 -*-
from .__version__ import (
    __title__, __description__, __url__, __version__,
    __author__, __author_email__, __license__
)

from .client import ETGClient
from .hotels import ETGHotelsClient
from .models import (
    Response, GuestData,
)
from .exceptions import (
    ETGException, BadRequestException, AuthErrorException, ProcessingStatusException,
)

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
