# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Esteban J. G. Gabancho.
#
# Flask-SSO-SAML is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Module tests."""

from __future__ import absolute_import, print_function

import os

import pkg_resources
import pytest
from flask import Flask
from mock import patch

from flask_sso_saml import FlaskSSOSAML
from flask_sso_saml.proxies import current_sso_saml


def test_version():
    """Test version import."""
    from flask_sso_saml import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = FlaskSSOSAML(app)
    assert 'flask-sso-saml' in app.extensions

    app = Flask('testapp')
    ext = FlaskSSOSAML()
    assert 'flask-sso-saml' not in app.extensions
    ext.init_app(app)
    assert 'flask-sso-saml' in app.extensions

    state = app.extensions['flask-sso-saml']
    assert state.prepare_flask_request
    assert callable(state.prepare_flask_request)


def test_app_config(appctx):
    """Test app settings builder."""
    settings_idp1 = current_sso_saml.get_settings('test-idp')

    assert settings_idp1['strict']
    assert settings_idp1['idp']['entityId'] == 'https://test-idp.com'

    # Handlers
    assert callable(current_sso_saml.get_handler('test-idp', 'login_handler'))
    assert callable(current_sso_saml.get_handler('test-idp', 'acs_handler'))
    assert current_sso_saml.get_handler('test-idp', 'settings_handler') is None

    settings_idp2 = current_sso_saml.get_settings('idp-file')

    assert settings_idp2['idp']['entityId'] == "https://login.idp.com"
    assert settings_idp2['sp']['x509cert'] == 'crt\n'
    assert settings_idp2['sp']['privateKey'] == 'key\n'

    reponse_file = pkg_resources.resource_filename(
        __name__, os.path.join('data', 'idp.xml'))
    with open(reponse_file, 'r') as f:
        response = f.read()

    with patch('onelogin.saml2.idp_metadata_parser.urllib2.urlopen'
               ) as urlopen_mock:
        urlopen_mock.return_value = type(
            'Response', (), {
                'read': lambda *args, **kwargs: response
            })()
        settings_idp2 = current_sso_saml.get_settings('idp-url')
        assert settings_idp2['idp']['entityId'] == "https://login.idp.com"


def test_auth(appctx, metadata_response):
    """Test Auth class."""
    with appctx.test_request_context(), pytest.raises(KeyError):
        auth = current_sso_saml.get_auth('wrong-idp')

    with appctx.test_request_context():
        auth = current_sso_saml.get_auth('test-idp')
        assert auth
        assert auth.idp == 'test-idp'
