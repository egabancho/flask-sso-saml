# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Esteban J. G. Gabancho.
#
# Flask-SSO-SAML is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension that provides SSO SAML integration."""

from __future__ import absolute_import, print_function

from .ext import FlaskSSOSAML
from .version import __version__

__all__ = ('__version__', 'FlaskSSOSAML')
