:sequential_nav: both

.. _tutorial-setup-project-locally:
.. _replicate-project-locally:


..  include:: /introduction/includes/03-local-1-set-up.rst


Install Python and Django using the ``Dockerfile``
--------------------------------------------------

This application requires that we have Python installed in the container. By using an official Docker base image that
includes Python, we can speed up build times and rely on a lightweight and expertly-constructed foundation. The
``Dockerfile`` that defines the application is currently empty. We will use Python 3.8, so add:

..  code-block:: Dockerfile

    FROM python:3.8

This will use the official Docker ``python`` base image as the foundation for everything else that we build on top.

Let's check that Docker can build an image from our newly-created Dockerfile, by running:

..  code-block:: bash

    docker build .

This application will use Django 3.1.x. We can install Django and its Python dependencies by using ``pip`` to process a
list of requirements. Create a new file ``requirements.txt`` in the application and list Django:

..  code-block:: text

    django>=3.1,<3.2

The requirements file needs to be made accessible *inside* the Docker application. So, we will copy it (and everything
else in the root of this application) into the image's filesystem at ``/app`` (it doesn't need to be there in 
particular, but ``/app`` is a useful convention), and for convenience, we can set Docker to use ``/app`` as its base 
directory. Finally, we will run the ``pip`` command.

..  code-block:: Dockerfile
    :emphasize-lines: 2-

    FROM python:3.8
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt

Check again that the application builds as expected with ``docker build .``.


Create a ``docker-compose.yml`` file for convenience
-------------------------------------------------------

The ``docker`` command is concerned merely with images and containers - not applications as a whole. An application
will typically include a number of components and resources, such as a database and media storage as well as code, and
all these various parts need to be orchestrated to function as an application. Docker Compose provides a very
convenient way to manage and interact with Docker applications. For example, it's convenient to have port-mapping set
up locally, and to have direct access to files inside the container while developing.

``docker-compose.yml`` configures Docker Compose. Create a new ``docker-compose.yml`` file in the application:

..  code-block:: YAML

    version: "2"

    services:

      web:
        # the application's web service (container) will use an image based on our Dockerfile
        build: "."
        # map the internal port 80 to port 8000 on the host
        ports:
          - "8000:80"
        # map the host directory to app (which allows us to see and edit files inside the container)
        volumes:
          - ".:/app:rw"
        # the default command to run whenever the container is launched
        command: python manage.py runserver 0.0.0.0:80

This now provides a convenient way to run commands inside the Dockerised environment, and also gives us access to a
number of useful ``docker-compose`` commands. For example, now you can use ``docker-compose build`` to build the entire
application, not just one image, and to run commands inside the application. Try ``docker-compose build`` now.


Create a new Django application in the application
--------------------------------------------------

Next we need to create a new Django project in the application (with ``django-admin startproject``), so run:

..  code-block:: bash

    docker-compose run web django-admin startproject myapp .

This starts up a container (``web``, which according to ``docker-compose.yml`` will be based on the ``Dockerfile`` in
the same directory) and executes the ``django-admin`` command inside it. It's important to note that the command is
executed inside the Docker application environment, and not in the host environment.

The command will add a new ``myapp`` directory and a ``manage.py`` file. Although they were created *inside* the
container, so you wouldn't normally be able to see them, the ``volumes`` directive in the ``docker-compose.yml`` file
maps ``/app`` to the host filesystem, so you can see them and edit them without having to be inside the Docker
environment yourself.


Start the local application
-------------------------

Start the application by running ``docker-compose up`` in the terminal::

    ➜  docker-compose up
    Starting tutorial-project_web_1 ... done
    Attaching to tutorial-project_web_1
    web_1  | Watching for file changes with StatReloader

Open the application in your web browser by visiting http://127.0.0.1:8000, where you should see the default Django 
success page.

Notice above that although the Django runserver is running on port 80, the application is accessible on port 8000. The
``docker-compose.yml`` configuration file is responsible for :ref:`this port-mapping <docker-compose-web>`.

If you amend or even just save any Python file in the Django project, the runserver will reload the Python modules and
restart.


Add a start-up instruction to the ``Dockerfile``
------------------------------------------------

Docker Compose is only used locally, not in our cloud deployments. Moreover, the Django runserver that we're using here
is fine for local development but unsuitable for use in production. For production, we will use `uWSGI
<https://uwsgi-docs.readthedocs.io>`_ (uWSGI is a WSGI gateway server for Python).

Add:

..  code-block:: text

    uwsgi==2.0.19.1

to ``requirements.txt``. These dependencies are baked into the image, so every time you amend the requirements, you
will need to rebuild with the new dependency list (we'll do that in a moment).

The Django application can be started with uWSGI. This should be baked into the ``Dockerfile`` itself, as a start-up 
command. To the end of the file, add:

..  code-block:: Dockerfile

    CMD uwsgi --module=myapp.wsgi --http=0.0.0.0:80

Run:

..  code-block:: bash

    docker-compose build

once more. Now when the web container is launched it will run the command automatically, to start it up in - for
example - a cloud deployment.

However, when we start it locally with ``docker-compose up``, the ``command`` line in the ``docker-compose.yml`` file
overrides that, and uses ``python manage.py runserver 0.0.0.0:80`` instead.

Try running the application locally using uWSGI rather than the runserver, by temporarily commenting out the ``command``
line in the ``docker-compose.yml`` file. Note that it's not necessary to rebuild after making changes to
``docker-compose.yml`` - Docker Compose uses images, but doesn't affect what's in them.

Restore the ``command`` line in the ``docker-compose.yml`` file before continuing.


..  include:: /introduction/includes/03-local-2-useful-commands.rst


..  code-block:: bash

    docker-compose run web python manage.py shell

which will open a Django shell in the ``web`` container.


..  include:: /introduction/includes/03-local-3-next.rst
