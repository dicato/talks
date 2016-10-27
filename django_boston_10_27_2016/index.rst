Adding Two-Factor Authentication to Django (with ``django-allauth``)
####################################################################

Django Boston

October 27, 2016

Patrick Cloke

Who am I?
=========

.. image:: clokep.jpg
    :align: right
    :scale: 50%

Patrick Cloke

* Lead Software Engineer @ Percipient Networks working on Strongarm (https://strongarm.io)
* `Mozillian <https://mozillians.org/u/clokep/>`_ (Instantbird & Mozilla Thunderbird instant messaging)
* `github.com/clokep <https://github.com/clokep>`_ / `bitbucket.com/clokep <https://bitbucket.org/clokep/>`_
* `@clokep on Twitter <https://twitter.com/clokep>`_
* http://patrick.cloke.us

.. image:: strongarm_logo.png
    :align: center

Two-factor (multi-factor) authentication [#]_ [#]_
==================================================

Two-factor / mutli-factor / 2FA:
    Requiring a login to have multiple pieces of evidence that a user owns an
    account.

.. figure:: SecureID_token_new.JPG
    :align: right
    :scale: 30%

Requires two pieces of evidence:

1. Knowledge (something the user knows): e.g. a password, passphrase, PIN.
2. Possession (something the user has): e.g. RSA SecureID, mobile devices / soft
   token, smart cards.
3. Inherence (something the user is): e.g. biometrics: fingerprint, retina, or
   voice.

.. [#] `Multi-factor authentication <https://en.wikipedia.org/wiki/Multi-factor_authentication>`_ on Wikipedia
.. [#] `SecureID token new.JPG <https://commons.wikimedia.org/wiki/File:SecureID_token_new.JPG>`_ on Wikimedia Commons, released into Public Domain

Two-factor (multi-factor) authentication
========================================

Generally the second factor is a user's phone via one of two mechanisms:

.. image:: microsoft-authenticator.png
    :align: right
    :scale: 12%

* TOTP (Time-based One-Time Password Algorithm)  [#]_, e.g. Google Authenticator,
  Microsoft Authenticator, Facebook Code Generator, etc. (See :rfc:`6238`.)
* SMS / Text message

.. warning::

    * Showing SMS messages on mobile phone lock screens allows easy bypassing of
      two-factor authentication.
    * Receiving emails (i.e. password reset emails) on a mobile phone recombines
      the two-factors back to a single factor.

.. [#] `Time-based One-time Password Algorithm <https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm>`_ on Wikipedia

Why Django?
===========

I assume you know what Django is...but just a few reasons we love it:

.. image:: django-logo-negative.png
    :align: right
    :scale: 25%

* "Batteries included"
* Django is extremely flexible!
* Tons of great reusable packages from the Django community!
* ...lots of other reasons... [#]_

.. [#] `Why Django? <https://www.djangoproject.com/start/overview/>`_

``django-allauth`` [#]_
=======================

Package to work with authentication, registration, account management, and
social authentication. [#]_

* Supports both local (i.e. ``django.contrib.auth``) and "social" accounts (e.g.
  OpenID, OAuth, OAuth2 providers)

    * Many social providers come pre-packaged (e.g. GitHub, Amazon, Twitter)

* Pluggable (you can add custom providers)
* Supports multiple providers in the same Django application
* Supports multiple options for account verification

.. [#] |django-allauth|_
.. [#] `Welcome to django-allauth: Rationale <https://django-allauth.readthedocs.io>`_

.. |django-allauth| replace:: ``django-allauth`` on GitHub
.. _django-allauth: https://github.com/pennersr/django-allauth>

``django-allauth-2fa`` [#]_
===========================

A reusable package that adds two-factor authentication to ``django-allauth``. It
provides the glue between ``django-otp`` [#]_ and ``django-allauth``.

* Views and middleware to modify the login workflow.
* Views for enabling/disabling two-factor authentication.
* Support for "backup" codes.
* Works with Django 1.8, 1.9, 1.10, and ``master``.

.. [#] |django-allauth-2fa|_
.. [#] |django-otp|_

.. |django-allauth-2fa| replace:: ``django-allauth-2fa`` on GitHub
.. _django-allauth-2fa: https://github.com/percipient/django-allauth-2fa
.. |django-otp| replace:: ``django-otp`` on BitBucket
.. _django-otp: https://bitbucket.org/psagers/django-otp/

.. ..

    Most of the magic is done via django-allauth and django-otp, we're just
    lining up the interfaces. (And making it easy to configure.)

Example Workflow (1/2): User login
==================================

A user enters their username & password, like normal.

.. image:: login-1.png
    :align: center

Example Workflow (2/2): User login
==================================

* The user is prompted for their two-factor token.
* If successful, they are logged in as normal!

.. image:: login-2.png
    :align: center

Example Workflow (1/3): Configuring Two-Factor
==============================================

* Users are presented with a QR code for enabling two-factor authentication.
* This supports devices which can take a picture of the QR code (e.g. Google
  Authenticator, Microsoft Authenticator).

.. ..

    This can be set to 85% if on widescreen.

.. image:: setup-1.png
    :align: left
    :scale: 65%

.. image:: microsoft-authenticator-setup.png
    :align: right
    :scale: 10%

Example Workflow (2/3): Configuring Two-Factor
==============================================

Once a user has two-factor enabled, they can:

* Disable it
* Create backup codes

.. image:: setup-2.png
    :align: center

Example Workflow (3/3): Configuring Two-Factor
==============================================

* Backup codes are displayed if they've been generated.
* Backup codes can be used only once.

.. image:: setup-3.png
    :align: center

How do I set it up? (1/6)
=========================

Install the package via pip [#]_.

.. code-block:: bash

    pip install django-allauth-2fa

.. [#] Ideally you're using a |virtualenv|_! That could be an entire separate
       lightning talk.

.. |virtualenv| replace:: ``virtualenv``
.. _virtualenv: https://virtualenv.pypa.io/en/stable/

How do I set it up? (2/6)
=========================

* Add ``django-allauth-2fa`` to the list of installed apps in ``settings.py``.
* (Also add ``django-allauth``, ``django-otp``, and their dependencies.)

.. code-block:: python
    :linenos:
    :emphasize-lines: 11

    INSTALLED_APPS = (
        'django.contrib.sites',  # Required by allauth.
        'django.contrib.auth',  # Configure Django auth package.
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'allauth',  # Enable allauth.
        'allauth.account',
        'django_otp',  # Configure the django-otp package.
        'django_otp.plugins.otp_totp',
        'django_otp.plugins.otp_static',
        'allauth_2fa',  # Enable two-factor auth.
    )

How do I set it up? (3/6)
=========================

Enable the ``django-allauth-2fa`` middleware in ``settings.py``. [#]_

.. code-block:: python
    :linenos:
    :emphasize-lines: 9-12

    MIDDLEWARE_CLASSES = (
        # Configure Django auth package.
        'django.contrib.auth.middleware.AuthenticationMiddleware',

        # Configure the django-otp package. Note this must be after the
        # AuthenticationMiddleware.
        'django_otp.middleware.OTPMiddleware',

        # Reset login flow middleware. If this middleware is included, the login
        # flow is reset if another page is loaded between login and successfully
        # entering two-factor credentials.
        'allauth_2fa.middleware.AllauthTwoFactorMiddleware',
    )

.. [#] ``django-allauth-2fa`` also supports the ``MIDDLEWARE`` setting from
       Django>=1.10 as of `two days ago <https://github.com/percipient/django-allauth-2fa/pull/33>`_.

How do I set it up? (4/6)
=========================

Configure ``django-allauth`` to use the ``django-allauth-2fa`` adapter in
``settings.py``. (This enables the two-factor authentication login workflow.)

.. code-block:: python
    :linenos:
    :emphasize-lines: 1-2

    # Set the allauth adapter to be the 2FA adapter.
    ACCOUNT_ADAPTER = 'allauth_2fa.adapter.OTPAdapter'

    # Configure your default site. See
    # https://docs.djangoproject.com/en/dev/ref/settings/#sites.
    SITE_ID = 1

How do I set it up? (5/6)
=========================

* Add the ``django-allauth-2fa`` URLS to a ``urls.py`` file.
* Suggest doing it next to the allauth URLs.

.. code-block:: python
    :linenos:
    :emphasize-lines: 5

    from django.conf.urls import include, url

    urlpatterns = [
        # Include the allauth and 2FA urls from their respective packages.
        url(r'^', include('allauth_2fa.urls')),
        url(r'^', include('allauth.urls')),
    ]

How do I set it up? (6/6)
=========================

* You'll need to migrate your models before using ``django-allauth-2fa``.
*  ``django-allauth-2fa`` doesn't include models or migrations, but
   ``django-allauth`` and ``django-otp`` do.

.. code-block:: bash
    :linenos:

    python manage.py migrate

Collaborators Wanted
====================

* More testing needed (different configurations, interaction with social accounts)
* Support for more device types (e.g. HOTP, YubiKey, Twilio)
* Support for multiple devices per user
* Improving the documentation (e.g. add a quickstart document)
* Setting up and adding translations
* Any other feedback you might have!

https://github.com/percipient/django-allauth-2fa/

https://pypi.python.org/pypi/django-allauth-2fa/

.. ..

    No prior experience needed!

Thank You!
==========

Please reach out if you have any questions!

Patrick Cloke

`patrick@strongarm.io <patrick@strongarm.io>`_

Additionally, we're hiring!

https://strongarm.io/careers/

Slides available at https://github.com/percipient/talks/

.. image:: strongarm_logo.png
    :align: center
