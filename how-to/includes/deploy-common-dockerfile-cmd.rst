``EXPOSE`` and ``CMD``
~~~~~~~~~~~~~~~~~~~~~~~

``EXPOSE`` informs Docker that the container listens on the specified ports at runtime; typically, you'd need:

..  code-block:: Dockerfile

    EXPOSE 80

Launch a server running on port 80 by including a ``CMD`` at the end of the ``Dockerfile``.
