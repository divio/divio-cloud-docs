How to use our API
================================================

We provide a REST API using `OpenAPI <https://www.openapis.org>`_.

..  note::

    Our Control Panel API is currently provided on an as-is basis. The API is scheduled for a full public
    release, but until then must be regarded as unstable and subject to change.

    By design, the API will work only with projects that belong to an organisation. Projects under an user's
    *Personal* space will not be fully accessible via the API.


Create a Divio account for use with the API
-------------------------------------------

..  warning::

    The API allows destructive operations to be carried out. Although you can, we strongly recommend that you **do not
    use your own account/access token with the API**, and especially not with code that is in development or not fully
    tested.

We recommend that you create a dedicated account for use with the API, and minimise the access it is granted. For
example - where possible - rather than granting the account access to multiple organisations, give it access to just
one, and do not give it admin access unless this is necessary.


Connecting to the API
----------------------

The API's end-point is https://api.divio.com/apps/v3/.

You will need a suitable client to connect to the API. This could be the ``curl`` command or another application.


Authentication
~~~~~~~~~~~~~~

Each request made to the API must contain a valid Divio Control Panel access token. You can obtain an account's access
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
