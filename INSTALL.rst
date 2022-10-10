Installation
============


Requirements
------------

The `python3-saml <https://github.com/onelogin/python3-saml>`_ library uses
`xmlsec <https://github.com/mehcode/python-xmlsec>`_, which requires
``libxml2 >= 2.9.1`` and ``libxmlsec1 >= 1.2.14``. Both requirements can be
installed your favorite package manager.
For Debian you can use:

.. code-block:: console

   $ apt-get install libxml2-dev libxmlsec1-dev libxmlsec1-openssl

And for macos:

.. code-block:: console

   $ brew install libxml2 libxmlsec1

If you encounter any error during this process, please refer to the
documentation of the aforementioned libraries.


Flask-SSO-SAML is on PyPI so all you need is:

.. code-block:: console

   $ pip install flask-sso-saml

The latest development version can be installed from GitHub:

.. code-block:: console

   $ pip install git+git://github.com/egabancho/flask-sso-saml
