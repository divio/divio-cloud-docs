.. _debug-failed-deployment:

How to identify the root cause of a failed deployment
=====================================================

You will sometimes encounter a failed deployment on your Test or Live server, or a build failure
locally.


Test/Live server deployments
----------------------------

First, check that the deployment really has failed. Sometimes a site will fail to start up, but
this doesn't necessarily indicate a deployment failure.

A failed deployment will show you a *Last deployment failed* message in the Control Panel, and a
link to the deployment log:

.. image:: /images/deployment-failed.png
   :alt: 'Deployment failed, check log'
   :width: 408

(If your site is not working after a deployment, but you don't see such a message, see
:ref:`successful-deployment-failed-startup` below.)

Open the deployment log. The end of the log will provide the final error, though you will usually
then need to read back up to find more details.


.. _successful-deployment-failed-startup:

Successful deployment, failed start-up
--------------------------------------

Sometimes there is no failed deployment log, but the site fails to start. This is usually caused
by a programming error that becomes apparent at runtime. In this case, the error will be shown
in the site's runtime logs (available from the Control Panel).


Typical failures
----------------

Dependency conflict
~~~~~~~~~~~~~~~~~~~

Example error::

    Could not find a version that matches Django<1.10,<1.10.999,<1.11,<1.12,<1.9.999,<2,
    <2.0,==1.9.13,>1.3,>=1.11,>=1.3,>=1.4,>=1.4.10,>=1.4.2,>=1.5,>=1.6,>=1.7,>=1.8

Packages in your project specified conflicting dependencies. In the example above, there is no
version of Django that matches the constraint ``>=1.11`` and also several of the others.

This can happen when you have specified versions of packages that themselves require conflicting
versions of some other package. Often, especially in a project that used to work, it's caused by an
unpinned requirement, that then demands an unexpected dependency.

We can see from the error that ``Django>=1.11`` is the problem, so we can search through the log to
find what added it:

..  code-block:: text

    adding Django>=1.11
      from django-phonenumber-field==2.0.0

A search for ``adding django-phonenumber-field`` reveals:

..  code-block:: python

    adding django-phonenumber-field>=0.7.2
      from aldryn-people==1.2.2

So ``django-phonenumber-field`` isn't pinned adequately in Aldryn People.

The solution is to pin any packages to versions that have compatible dependencies, either in the
project's ``requirements.in``, or (if possible) in the ``setup.py`` of the other packages that
installed them::

    django-phonenumber-field<2.0.0

Locally, the project can be tested for dependency conflicts of this sort by running
``docker-compose build web``.


The website is locked
~~~~~~~~~~~~~~~~~~~~~

Example error: ``Locked: website-lock-27441 is locked``.

This usually happens when the Control Panel has set a flag for the site for deployment, and the
flag has not been lifted.

Generally the lock will time out by itself, but contact our support if you need it more quickly.


Site launch error
~~~~~~~~~~~~~~~~~

Example::

    Step 8/8 : RUN DJANGO_MODE=build python manage.py collectstatic --noinput
    [...]
    ImportError: No module named django_select2

In this case the site has been built successfully, but one of its launch routines (in this case
``collectstatic``) failed due to a programming error. The traceback will show where it occurred.
