.. _divio-project-environments:

Application environments
========================

Each Divio application includes three environments for the application by default.

The three environments are created in Docker containers from the same images.

* *Local*, running on your own computer
* *Test*, running on our Cloud servers
* *Live*, running on our Cloud servers

In our recommended workflow, development is done locally, before being deployed to *Test*
and finally to *Live*.

It is also possible to set up multiple cloud environments for an application. For example, a common scheme is to use 
four: *Development*, *Testing*, *QA*, *Production*.


.. _default-project-conditions:

Default application conditions
------------------------------

Some of these conditions may be readily altered according your needs, for example the ``DEBUG``
setting. See also :ref:`local-in-live-mode`.

+----------------------------------+------------------+----------------------------+---------------------------+
|                                  | Local            | Test                       | Live                      |
+==================================+==================+============================+===========================+
| ``STAGE`` environment variable   | ``local``        | ``test``                   | ``live``                  |
+----------------------------------+------------------+----------------------------+---------------------------+
| ``DEBUG`` environment variable   | ``True``         |``True``                    | ``False``                 |
+----------------------------------+------------------+----------------------------+---------------------------+
| static files served by           | local server     |  uWSGI                                                 |
+----------------------------------+ (e.g. Python     +----------------------------+---------------------------+
| media files served by            | runserver)       | our Cloud S3 service                                   |
+----------------------------------+------------------+----------------------------+---------------------------+
| database runs in                 | a local container| our Cloud database cluster                             |
+----------------------------------+------------------+----------------------------+---------------------------+
| number of application containers | one                                according to subscription              |
+----------------------------------+------------------+----------------------------+---------------------------+
| application container sleeps     | n/a              | after 15 minutes' activity | never                     |
+----------------------------------+------------------+----------------------------+---------------------------+
