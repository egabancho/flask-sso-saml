# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Esteban J. G. Gabancho.
#
# Flask-SSO-SAML is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import base64
import os
import sys

import pkg_resources
import pytest
from flask import Flask
from onelogin.saml2.utils import OneLogin_Saml2_Utils as saml_utils

from flask_sso_saml import FlaskSSOSAML

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode


@pytest.fixture(scope='module')
def app():
    """Flask application fixture with FLask-SSO-SAML initialized."""
    app = Flask('testapp')
    app.config.update(
        TESTING=True,
        SECRET_KEY='test-secret-key',
        SERVER_NAME='localhost',
        SSO_SAML_DEFAUTL_LOGIN_HANDLER=lambda auth, next_url: next_url,
        SSO_SAML_IDPS={
            'test-idp': {
                'settings': {
                    'idp': {
                        'entityId': 'https://test-idp.com',
                        'singleSignOnService': {
                            'url': 'https://test-ipd.com/sso',
                        },
                        'singleLogoutService': {
                            'url': 'https://test-ipd.com/slo',
                        },
                        'x509cert': 'cert'
                    }
                },
                'acs_handler': lambda auth, next_url: next_url,
            },
            'idp-file': {
                'settings_file_path':
                pkg_resources.resource_filename(
                    __name__, os.path.join('data', 'idp.xml')),
                'sp_cert_file':
                pkg_resources.resource_filename(
                    __name__, os.path.join('data', 'cert.crt')),
                'sp_key_file':
                pkg_resources.resource_filename(
                    __name__, os.path.join('data', 'cert.key')),
            },
            'idp-url': {
                'settings_url': 'https://test-idp.com/settings'
            },
        })
    FlaskSSOSAML(app)
    return app


@pytest.fixture(scope='module')
def appctx(app):
    """Application context for the current application."""
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def sso_response():
    """Mock SSO response from Identity Provider."""
    xml_file = pkg_resources.resource_filename(
        __name__, os.path.join('data', 'sso_response.xml'))
    with open(xml_file, 'rb') as f:
        return base64.b64encode(f.read())


@pytest.fixture(scope='module')
def slo_query_string():
    """Mock SLO response from Identity Provider."""
    xml_file = pkg_resources.resource_filename(
        __name__, os.path.join('data', 'slo_response.xml'))
    with open(xml_file) as f:
        slo_response = saml_utils.deflate_and_base64_encode(f.read())
    return urlencode(dict(SAMLResponse=slo_response))


@pytest.fixture(scope='module')
def metadata_response():
    """Metadata response."""
    xml_file = pkg_resources.resource_filename(
        __name__, os.path.join('data', 'metadata.xml'))
    with open(xml_file, 'rb') as f:
        return f.read()
