File-building operations
~~~~~~~~~~~~~~~~~~~~~~~~

If the application needs to perform any build operations to generate files, they should be run in the ``Dockerfile`` so
that they are built into the image. This could include compiling or collecting JavaScript or CSS, for example, and
can make use of frameworks that do this work.