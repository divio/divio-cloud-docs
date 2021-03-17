Install application-level dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Do the same for application-level dependencies, e.g.:

..  code-block:: Dockerfile

    # install dependencies listed in the repository's requirements file
    RUN pip install -r requirements.txt

Any requirements should be pinned as firmly as possibble.
