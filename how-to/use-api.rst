How to use our API
================================================

..  note::

    Our Control Panel API is currently provided on an as-is basis. The API is scheduled for a full public
    release, but until then must be regarded as unstable and subject to change.

    By design, the API will work only with projects that belong to an organisation. Projects under an user's
    *Personal* space will not be fully accessible via the API.

We provide a REST API, using `Swagger <https://swagger.io>`_ version 3 and the `OpenAPI <https://www.openapis.org>`_
specification.

A specification (machine-readable and human-readable) specifcation for the API is published at
https://cp-api-ref-stage.us.aldryn.io.


Connecting to the API
----------------------

The APU's end-point is https://api.divio.com/apps/v3/.

You will need a suitable client to connect to the API. This could be the ``curl`` command or another application.


Authentication
~~~~~~~~~~~~~~

Each request made to the API must contain a valid Divio Control Panel access token. You can obtain your own access
token from https://control.divio.com/account/desktop-app/access-token/.

..  warning::

    The access token grants extensive access to you projects on our platform. Never share your access token with any
    other user. If you need to use it in an application or script, it is your responsibility to ensure that it is
    transmitted and stored safely.

The token must be included in a header ``authorization``, in the form::

    Token <include your token>


Basic requests
--------------------------

A example using ``curl``::

    curl https://api.dev.aldryn.net/apps/v3/ -H 'authorization: Token yFagta25sbsus8d9JK9DrJCSKinqSWAoxU7NgN7IamtheCscry6jFfk3kingofthedivannTyYa10iqqD7EY5nvPR6yN47'

Here, the ``-H`` flag is used to pass the ``authorization`` header.

The principle using a dedicated REST API client, which will offer you more convenient ways to browse API, is much the
same, whether it provides a graphical or command-line interface. It will behave in much the same way: you need to
specify the URL, and provide the expected header.

The result of the command above will be a JSON response, something like::

    {
        "applications": "https://api.dev.aldryn.net/apps/v3/applications/",
        "environments": "https://api.dev.aldryn.net/apps/v3/environments/",
        "domains": "https://api.dev.aldryn.net/apps/v3/domains/",
        "patches": "https://api.dev.aldryn.net/apps/v3/patches/",
        "repositories": "https://api.dev.aldryn.net/apps/v3/repositories/",
        "serviceinstances": "https://api.dev.aldryn.net/apps/v3/serviceinstances/",
        "deployments": "https://api.dev.aldryn.net/apps/v3/deployments/",
        "builds": "https://api.dev.aldryn.net/apps/v3/builds/",
        "regions": "https://api.dev.aldryn.net/apps/v3/regions/"
    }


Using UUIDs to retrieve objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At each of these URLs, some meta-data and a list of available objects will be provided. Each object's UUID will be
shown; this can be appended to the URL to retireve further information about a particular object, for example:

    https://api.dev.aldryn.net/apps/v3/applications/l33t2jdmbrhhrlf6yherrnn7g4


Using parameters
~~~~~~~~~~~~~~~~

The interface for each of these endpoints is described at https://cp-api-ref-stage.us.aldryn.io; for example, for
``applications``, see https://cp-api-ref-stage.us.aldryn.io/#tag/applications. This lists the available query
parameters and their type, along with an optional description:

``name_search``: *string*
``slug``: *string*
``page``: *integer* (A page number within the paginated result set.)

This means that you can search for an application (i.e. a Divio Cloud project) containing the name *PyCon*::

    https://api.dev.aldryn.net/apps/v3/applications?name_search=PyCon

or find the application whose exact slug is *pycon-africa*::

    https://api.dev.aldryn.net/apps/v3/applications?slug=pycon-africa

These queries can be combined in the usual way::

    https://api.dev.aldryn.net/apps/v3/endpoint?query_name_1=my_first_query&query_name_2=my_second_query
