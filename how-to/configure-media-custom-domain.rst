..  _how-to-configure-media-serving-custom-domain:

How to configure media serving on a custom domain
=================================================

By default, media files in Divio projects are served directly from our S3 cloud storage service,
and the URL of each object will refer to that storage endpoint - for example, objects may be served
from an S3 bucket which might have a domain like:
``example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io``.

Some users may prefer or require that their media are served from their own domain, say
``media.example.com``.

This is not an option available by default, but it can be configured by setting up a reverse proxy.


Set up the reverse proxy project
----------------------------------

Create a new Divio project, using the options:

* *Python*: ``No platform``
* *Project type*: ``Nginx``

This project will contain the reverse proxy, that will refer all requests made to the custom domain
to the actual domain that the application serves its media from. The only function of this reverse
proxy project is to refer requests to the actual application project.


Set up a domain for media files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using the Control Panel, add the domain to the reverse proxy project.


Configure Nginx as a reverse proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We expect users who adopt this approach to be familiar with the management of reverse proxies
and comfortable with their configuration. It's beyond the scope of our support to provide details
of how this should be done, however:

* set up the Nginx configuration to proxy requests from (say) ``media.example.com`` to (say)
  ``example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io``
* you *may* also need to configure header rewriting; some S3 hosts are stricter than others and
  may refuse to accept requests with the wrong heads

Deploy the project and check that requests for media objects on the custom domain are correctly
referred to the actual storage, and that they are served as expected.


Configure media storage URLs in the application project
--------------------------------------------------------------------

Your application has an automatically-configured :ref:`DEFAULT_STORAGE_DSN
<storage_access_details>` environment variable. This contains the domain used by your code (e.g.
Django Storages, for Django templates and views) when it needs to refer to the URL of a media
object.

You will need to adapt this value, substituting the custom domain you wish to use, and
apply it manually in the *Environment Variables* section of the project's dashboard. Then the
application project will need to be redeployed.

..  note::

    As far as your application is concerned, it will still interact with the storage bucket,
    using the storage backend, at the original address. It is only when it needs to use a URL
    to refer to objects for access over HTTP that it will use the custom domain.


Caveats
-------

When using our automatically-configured ``DEFAULT_STORAGE_DSN``, you don't need to be concerned
about keeping this up-to-date - it's managed for you.

When using your own custom domain, you will need to manage the configuration. For example, if your
project is redeployed to a different region, the URL for its storage could change, and both the
Nginx configuration and the ``DEFAULT_STORAGE_DSN`` will need to be changed too.
