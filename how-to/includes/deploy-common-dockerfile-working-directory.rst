``WORKDIR``
~~~~~~~~~~~

We recommend setting up a working directory early on in the ``Dockerfile`` before you need to write any files, for
example:

..  code-block:: Dockerfile

    # set the working directory
    WORKDIR /app
    # copy the repository files to it
    COPY . /app
