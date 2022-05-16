.. _configure-ci:

How to configure a CI/CD Deployment service
=======================================================================

Continuous Integration/Continuous Delivery is a powerful addition to your development workflow. CI/CD automates
deployment of commits that have passed tests and been merged into the deployment branch.


The basic principles
--------------------

When a build completes successfully on the CI service, it needs to send a signal to the Control Panel to start the
deployment. Typically this would be with the command::

    divio app deploy --remote-id <website id>

where the ``<website id>`` is as shown in its Divio Control Panel dashboard URL.

The Divio CLI will need to be installed in the environment that executes this command, and to be authenticated with
the Control Panel.


An example using Travis CI
--------------------------

In this example we will use `Travis CI <https://travis-ci.org>`_ as an example, though Circle CI, Jenkins and
other services will work just as well, and the principles are the same.


Connect your application to the CI service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For Travis, this means activating the application in your Travis account settings
(https://travis-ci.org/account/repositories).

Your application needs a ``.travis.yml`` file, which depending on the application might look something like::

    language: python

    python:
      - 3.5

    sudo: false

    install:
      - pip install isort flake8

    script:
      - flake8 --max-line-length=200


Triggering the deployment on success
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a build is successful, we need Travis to log in as a Divio user and execute some steps in the
``after_success`` section of the file:

* install the Divio CLI
* log in
* run a ``divio app deploy`` command, using your application's website id


Authentication
^^^^^^^^^^^^^^

To log in, Travis needs to provide `your Divio authentication token
<https://control.divio.com/account/desktop-app/access-token/>`_.

..  admonition:: **Never** include security keys in plain text

    The token must **never** be included in plain text in the repository. Instead, you need to use an encrypted
    version. We recommend creating a Divio account specifically for using with Travis, so that you can more
    easily manage and revoke access.

You can encrypt your token using `Travis's encrypt tool <https://docs.travis-ci.com/user/encryption-keys/>`_. Once you
have obtained the encrypted token, you can add the following to the ``travis.yml`` file::

    after_success:
       - pip install divio-cli
       - divio login <encrypted token>
       - divio app deploy --remote-id <website id>

You could also run::

    travis encrypt TOKEN="secretvalue" --add

which will add something like::

    env:
      global:
        secure: EsKcqn4H0EBqZhEts [...] X6klJCNI=

to the file, and make ``$TOKEN`` available as an environment variable. So you would then use::

    - divio login $TOKEN

in the file.


Using the deployment API directly
---------------------------------

The Divio CLI is the most elegant way of interacting with the Control Panel for deployment, but if desired, you can also
use the API directly::

    curl -X POST --data 'stage=<env-slug>' --header "Authorization: Basic <encrypted token>" https://control.divio.com/api/v1/website/<website id>/deploy/


Caveats
-------

* Multiple successive pull requests could lead to a race condition, depending on the order in which they arrive, in
  which a successful CI build triggers a deployment that then prevents the next build from deploying.
* If the CI job finishes very fast, it could trigger a deployment on the server before the Control Panel has had time
  to pull the changes to be deployed.
