..  admonition:: Use ``CMD``, not ``ENTRYPOINT``, to start the server

    A ``CMD`` that starts the server allows our infrastructure to override this default, for example to launch
    containers without starting the server, when some other process needs to be executed. 
    
    An ``ENTRYPOINT`` that starts the server would not allow this.

    If you are using a Docker entrypoint script, it's good practice to conclude it with ``exec "$@"``, `so that any
    commands passed to the container will be executed as expected <https://stackoverflow.com/a/39082923/2422705>`_.
