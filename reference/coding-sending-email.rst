.. _sending-email:

Sending email in Divio applications
===================================

Divio does not provide mail services. To send mail from your Django applications, you will
need to provide the appropriate configuration.

Django :doc:`provides email wrappers <django:topics/email>` around Python's ``smtplib`` module.


Configuration
-------------

The following configuration settings can be provided:

Basic settings
    ``EMAIL_HOST`` and ``EMAIL_PORT`` (defaults to ``25``)

Authentications settings
    ``EMAIL_HOST_USER`` and ``EMAIL_HOST_PASSWORD``

Secure authentication
    ``EMAIL_USE_TLS`` and ``EMAIL_USE_SSL``


.. _email-url:

Using ``EMAIL_URL`` environment variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

However, the preferred way to provide these is via an ``EMAIL_URL`` :ref:`environment variable
<environment-variables>`, so that your local, Test and Live servers can use their own configuration.

The ``EMAIL_URL`` is the recommended way of combining the settings into a single variable. For
example, suppose you have::

    EMAIL_HOST = smtp.example.com
    EMAIL_PORT = 25
    EMAIL_HOST_USER = janeausten
    EMAIL_HOST_PASSWORD = password

you can instead use::

    smtp://janeausten:password@smtp.example.com:25

For:

* TLS, add ``?tls=True`` (and use port 587)
* SSL, add ``?ssl=True`` (and use port 465)

to the URL. Note that *TLS is preferred*, and you can't use both.

The URL is parsed using the `dj-email-url library <https://github.com/migonzalvar/dj-email-url>`_.


Additional Django email settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some additional email settings are available in Django. These can be provided as environment
variables.

``DEFAULT_FROM_EMAIL``
    Allows you to specify a default ``From`` address for general automated messages from your
    website.

``SERVER_EMAIL``
    Specifies a default ``From`` address for error messages from your site.


Usage, testing and troubleshooting
----------------------------------

It's beyond the scope of this document to discuss usage in detail. The official :doc:`Django
documentation <django:topics/email>` has more information.

It's useful to be able to test your configuration. You can do this in your project's :ref:`local shell <local-shell>` or :ref:`Cloud shell <cloud-shell>`.

Once in the shell, launch the Django shell::

    python manage.py shell

Import the Django ``send_mail`` function::

    from django.core.mail import send_mail

and try sending a message::

    send_mail(
        "Welcome to Divio",
        "It's great!",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )

The email settings will be taken from the :ref:`EMAIL_URL environment variable <email-url>`, but
can be overwritten in the shell - for example::

    EMAIL_USE_TLS = True
