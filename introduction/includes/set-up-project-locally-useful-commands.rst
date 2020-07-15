Useful commands
----------------------------------------

So far, we have used the ``divio``, ``docker-compose`` and ``docker`` commands. It's good to have a basic familiarity
with them and what they do. As you proceed through this tutorial, you will inevitably encounter the occasional issue.
These commands will help you when this happens.

..  note::

    You will find several examples of useful commands listed in `our local commands cheat sheet
    <https://docs.divio.com/en/latest/reference/local-commands-cheatsheet.html>`_.


Using ``divio``
^^^^^^^^^^^^^^^

The ``divio`` command is used mainly to manage your local project's resources and to interact with our Control Panel.
You have already used ``divio project setup`` and ``divio project list``; you can also use it to do things like push
and pull database and media content. Try:

..  code-block:: bash

    divio project dashboard

See the :ref:`Divio CLI reference <divio-cli-ref>` for more.


Using ``docker``
^^^^^^^^^^^^^^^^

The ``docker`` command is mostly used to manage Docker processes, and Docker itself. Mostly, you'll never need to use
it, but it can be useful when you need to understand what Docker is doing on your machine, or for certain operations.
You have already used ``docker ps``. Try:

..  code-block:: bash

    docker info


Using ``docker-compose``
^^^^^^^^^^^^^^^^^^^^^^^^

The ``docker-compose`` command is used mainly to control and interact with your local project. You will mostly use it
to start the local project and open a shell in the local web container. You have already used ``docker-compose build``
and ``docker-compose up``.

Just for example, try:
