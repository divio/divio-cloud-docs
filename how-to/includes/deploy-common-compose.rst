Local container orchestration with ``docker-compose.yml``
---------------------------------------------------------------------

What's described above is fundamentally everything you need in order to deploy your application to Divio. You could
deploy your application with that alone.

However, you would be missing out on a lot of value. Being able to build and then run the same application, in a very
similar environment, locally on your own computer before deploying it to the cloud makes development and testing much
more productive. This is what we'll consider here.

..  admonition:: ``docker-compose.yml`` is **only** used locally

    Cloud deployments do not use Docker Compose. Nothing that you do here will affect the way your application runs
    in a cloud environment. See :ref:`docker-compose.yml <docker-compose-yml-reference>`.

Create a ``docker-compose.yml`` file, :ref:`for local development purposes <docker-compose-local>`. This will replicate
the ``web`` image used in cloud deployments, allowing you to run the application in an environment as close to that of
the cloud servers as possible. Amongst other things, it will allow the project to use a Postgres or MySQL database
(choose the appropriate lines below) running in a local container, and provides convenient access to files inside the
containerised application.

Take note of the highlighted lines below; some require you to make a choice.
