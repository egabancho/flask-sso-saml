# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Esteban J. G. Gabancho.
#
# Flask-SSO-SAML is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Minimal Flask application example.

SPHINX-START

1. Register your app OneLogin (you might choose any IdP of your liking):

   - ``https://0.0.0.0:5000/saml/acs/onelogin``: SAML Consumer URL
   - ``https://0.0.0.0:5000/saml/sls/onelogin``: SAML Single Logout URL
   - ``https://0.0.0.0:5000/saml/metadata/onelogin``: SAML Audience
   - ``https://0.0.0.0:5000/saml/acs/onelogin``: SAML Recipient

2. Ensure you have ``gunicorn`` package installed:

   .. code-block:: console

      pip install gunicorn

3. Ensure you have ``openssl`` installed in your system (Most of the Linux
   distributions has it by default.).

3. Grab the *Issuer URL*, *SAML 2.0 Endpoint (HTTP)*,
   *SLO Endpoint (HTTP)* and *X.509 Certificate* after registering the
   application (they are under the SSO tab) and add them to your instance
   configuration.

   .. code-block:: console

       $ export IDP_ENTITY_ID='https://app.onelogin.com/saml/metadata/....'
       $ export IDP_SSO_URL='https://myapp-dev.onelogin.com/trust/saml2/http-post/sso/....'
       $ export IDP_SLS_URL='https://myapp-dev.onelogin.com/trust/saml2/http-redirect/slo/....'
       $ export IDP_CERT='one_line_certificate'


4. Install Flask-SSO-SAML and setup the application by running:

   .. code-block:: console

       $ pip install -e .[all]
       $ cd examples
       $ ./app-setup.sh

5. Create the key and the certificate in order to run a HTTPS server:

   .. code-block:: console

       $ openssl genrsa 1024 > instance/ssl.key
       $ openssl req -new -x509 -nodes -sha1 -key instance/ssl.key > instance/ssl.crt

6. Run gunicorn server:

   .. code-block:: console

       $ gunicorn -b :5000 --certfile=./instance/ssl.crt --keyfile=./instance/ssl.key app:app

7. Open in a browser the page `<https://0.0.0.0:5000/>`_.

8. To reset the example application run:

   .. code-block:: console

       $ ./app-teardown.sh

SPHINX-END
"""

from __future__ import absolute_import, print_function

import os

import jinja2
from flask import Flask, redirect, render_template, session

from flask_sso_saml import FlaskSSOSAML


def login_handler(auth, next_url):
    """Reset session things."""
    session['success_slo'] = False
    return next_url


def acs_handler(auth, next_url):
    """Put user info in the session."""
    session['samlUserdata'] = auth.get_attributes()
    session['no_auth_warn'] = not auth.is_authenticated()
    return next_url


def sls_handler(auth, next_url):
    """Set sls in the session."""
    session['success_slo'] = False
    return next_url


def _get_attrs():
    """Get user attributes from the session."""
    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            return session['samlUserdata'].items()
    return None


# Create Flask application
app = Flask(__name__)

app.config.update(
    dict(
        SSO_SAML_IDPS={
            'onelogin': {
                'settings': {
                    'idp': {
                        'entityId': os.environ.get('IDP_ENTITY_ID'),
                        'singleSignOnService': {
                            'url': os.environ.get('IDP_SSO_URL')
                        },
                        'singleLogoutService': {
                            'url': os.environ.get('IDP_SLS_URL')
                        },
                        'x509cert': os.environ.get('IDP_CERT'),
                    },
                },
                'login_handler': login_handler,
                'acs_handler': acs_handler,
                'sls_handler': sls_handler,
            }
        },
        SERVER_NAME='0.0.0.0:5000',
        SECRET_KEY='EXAMPLE_APP',
    ))

# Set jinja loader to first grab templates from the app's folder.
app.jinja_loader = jinja2.ChoiceLoader([
    jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), "templates")), app.jinja_loader
])

FlaskSSOSAML(app)


@app.route('/')
def index():
    """Homepage."""
    attributes = _get_attrs()

    return render_template(
        'index.html',
        attributes=attributes,
        paint_logout=True if attributes else False,
        not_auth_warn=session.get('no_auth_warn'),
        success_slo=session.get('success_slo'),
    )


@app.route('/attrs')
def attrs():
    """User attributes."""
    attributes = _get_attrs()

    return render_template(
        'attrs.html',
        paint_logout=True if attributes else False,
        attributes=attributes)
