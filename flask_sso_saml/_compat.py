# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Esteban J. G. Gabancho.
#
# Flask-SSO-SAML is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Python 2/3 compatibility layer."""

from __future__ import absolute_import, print_function

import sys

PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
    from urllib.parse import urlparse
else:
    string_types = basestring
    from urlparse import urlparse
