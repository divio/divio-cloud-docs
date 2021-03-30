..  admonition:: Use ``CMD``, not ``ENTRYPOINT``, to start the server

    Using ``CMD`` provides a default way to start the server, that can also be overridden. This is useful when working
    locally, where often we would use the ``docker-compose.yml`` to issue a startup ``command`` that is more suited to
    development purposes. It also allows our infrastructure to override the default, for example in order to launch
    containers without starting the server, when some other process needs to be executed.

    An ``ENTRYPOINT`` that starts the server would not allow this.

    If you are using a Docker entrypoint script, it's good practice to conclude it with ``exec "$@"``, `so that any
    commands passed to the container will be executed as expected <https://stackoverflow.com/a/39082923/2422705>`_.
