.. _use-divio-api:

How to use the Divio API
================================================

We provide a REST API using `OpenAPI <https://www.openapis.org>`_.

`Divio API reference documentation <https://api.docs.divio.com>`_


Create an API-only account
---------------------------------------------------------

..  admonition:: The API allows destructive operations to be carried out.

    We strongly recommend that you **do not use your own account/access token with the API**, and
    especially not with code that is in development or not fully tested.

We recommend instead that you create a dedicated account for use with the API, and minimise the access it is granted.
For example - where possible - rather than granting the account access to multiple organisations, give it access to
just one, and do not give it admin access unless this is necessary.


Connecting to the API
----------------------

The API's end-point is https://api.divio.com/apps/v3/.

You will need a suitable client to connect to the API. This could be the ``curl`` command or another application.

Note that ``https://api.divio.com/apps/v3/`` doesn't require authorisation, but other URLs do. For example, if you
try ``https://api.divio.com/apps/v3/applications/`` and receive an *Unauthorised* error, that's because the credentials
you provided were not recognised.


Authentication
~~~~~~~~~~~~~~

Each request made to the API must contain a valid Divio Control Panel access token. You can obtain an account's access
token from https://control.divio.com/account/desktop-app/access-token/.

..  warning::

    The access token grants extensive access to you applications on our platform. Never share your access token with any
    other user. If you need to use it in an application or script, it is your responsibility to ensure that it is
    transmitted and stored safely.

The token must be included in a header ``authorization``, in the form::

    Token yFagta25sbsus8d9JK9DrJCSKinqSWAoxU7NgN7IamtheCscry6jFfk3kingofthedivannTyYa10iqqD7EY5nvPR6yN47


Basic requests
--------------------------

A example using ``curl``::

    curl https://api.divio.com/apps/v3/applications/ -H 'authorization: Token yFagta25sbsus8d9JK9DrJCSKinqSWAoxU7NgN7IamtheCscry6jFfk3kingofthedivannTyYa10iqqD7EY5nvPR6yN47'

Here, the ``-H`` flag is used to pass the ``authorization`` header.

The principle using a dedicated REST API client, which will offer you more convenient ways to browse API, is much the
same, whether it provides a graphical or command-line interface. It will behave in much the same way: you need to
specify the URL, and provide the expected header. If you are using a dedicated API client, then you could issue the
same request with:

* request type: *GET*
* request URL: ``https://api.divio.com/apps/v3/applications/``

and including a header:

* header name: ``authorization``
* header value: ``Token yFagta25sbsus8d9JK9DrJCSKinqSWAoxU7NgN7IamtheCscry6jFfk3kingofthedivannTyYa10iqqD7EY5nvPR6yN47``

The result of the command above will be a JSON response, for example::

    {
        "applications": "https://api.divio.com/apps/v3/applications/",
        "environments": "https://api.divio.com/apps/v3/environments/",
        "domains": "https://api.divio.com/apps/v3/domains/",
        "patches": "https://api.divio.com/apps/v3/patches/",
        "repositories": "https://api.divio.com/apps/v3/repositories/",
        "serviceinstances": "https://api.divio.com/apps/v3/serviceinstances/",
        "deployments": "https://api.divio.com/apps/v3/deployments/",
        "builds": "https://api.divio.com/apps/v3/builds/",
        "regions": "https://api.divio.com/apps/v3/regions/"
    }

Refer to the `Divio API reference documentation <https://api.docs.divio.com>`_ for structured reference information on
the API.


Example
--------

For example, to find out when the most recent backup of the database was made for a particular environment, first,
you'd obtain the application's UUID, via::

    https://api.divio.com/apps/v3/applications/?slug=example-application

If the application exists, it will return a list with one entry, including::

    "uuid":"<application UUID>"

This is the UUID of the application.

Then, you need to get all environments for that application::

    https://api.divio.com/apps/v3/environments/?application=<application UUID>

This will give you a list of environments. In that list, find the one whose ``slug`` value matches the name of the
environment (Test, Live, etc) of the environment you're interested in. Once again, you want the environment's UUID.
(Obviously, this is the kind of operation that is much easier to perform programmatically than it is for a human to do.)

Next, you need to retrieve a list of backups, via::

    https://api.divio.com/apps/v3/backups

This list may spread across several pages - you will need to loop over the entire list, until you find a backup with whose ``environment`` value matches the environment UUID you retrieved in the previous step. This backup will have a
UUID of its own.

Then you need to retrieve the list of service instance backups::

    https://api.divio.com/apps/v3/service-instance-backups

which again may spread over several pages. Once more, loop over that list to find the instances that interest you. As
well as having a ``backup`` value that needs to match the backup UUID from the previous step, each one will have a
``service-instance`` value, that can be used with::

    https://api.divio.com/apps/v3/service-instances/

to identify what exactly was included in the service instance backup (database, media storage, etc).

Finally::

    https://api.divio.com/apps/v3/service-instance-backups/<service instance backup UUID>

will contain timestamps and other metadata for the backup::

    {
    "uuid": "bagztldeadfdhlilnmpzx3twly",
    "backup": "vyn5jrwaenga7kzevilxs66hd4",
    "service_instance": "x3rgfx4ycrpokelrawxfmmrewu",
    "queued_at": "2021-03-01T02:11:22.025898Z",
    "started_at": "2021-03-01T02:36:37Z",
    "ended_at": "2021-03-01T02:36:39Z",
    "taken_at": "2021-03-01T02:36:37Z",
    "size": 303780,
    "errors": [],
    }

The chain of relations to get to this information is: application > environments > backups > service instance backups,
with a cross-reference to service instances.

It's not feasible to do some of these operations by hand, but the work required can be readily accomplished with a
custom script, especially when using tools designed to help navigate APIs of this kind.

