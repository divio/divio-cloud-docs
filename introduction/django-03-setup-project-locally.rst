.. _tutorial-setup-project-locally:
.. _replicate-project-locally:


..  include:: includes/03-local-1-set-up.rst


Install Python and Django using the ``Dockerfile``
--------------------------------------------------

This project requires that we have Python to be installed in the container. By using an official Docker base image that
includes Python, we can speed up build times and rely on a lightweight and expertly-constructed foundation. The
``Dockerfile`` that defines the project is currently empty. Add:

..  code-block:: Dockerfile

    FROM python

This will use the official Docker ``python`` base image as the foundation for everything else that we build on top.

Inside the container we will build the application at ``/app`` (it doesn't need to be there in particular, but ``/app``
is a useful convention). Set the working directory for subsequent commands in the ``Dockerfile`` to use this directory:

..  code-block:: Dockerfile
    :emphasize-lines: 2

    FROM python
    WORKDIR /app

At every stage you can stop to check that Docker can build an image from the Dockerfile:

..  code-block:: bash

    docker build .

This project will use Django. Django and other Python dependencies *could* be installed by running ``pip install`` in
the ``Dockerfile``:

..  code-block:: Dockerfile

    RUN pip install django==3.1

However this would quickly become quite unpleasant to deal with as the list of Python dependencies grows, so don't do
that. A better way is to create a new file ``requirements.txt`` in the project, and list any dependencies in it:

..  code-block:: text

    django==3.1

and in the ``Dockerfile``, add:

..  code-block:: Dockerfile
    :emphasize-lines: 3-

    FROM python
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt

This helps keep the ``Dockerfile`` clean and easy to work with, and also follows the conventions of a normal Python
project, in which requirements are listed neatly in a file of their own.

Check again that the project builds as expected with ``docker build .``.


Create a ``docker-compose.yml`` file for convenience
-------------------------------------------------------

``docker`` is concerned merely with images and containers - not applications as a whole. An application will typically
include a number of components and resources, such as a database and media storage as well as code, and all these
various parts need to be orchestrated to function as an application. Docker Compose provides a very convenient way to
manage and interact with Docker applications. For example, it's convenient to have port-mapping set up locally, and to
have direct access to files inside the container while developing.

``docker-compose.yml`` configures Docker Compose. Create a new ``docker-compose.yml`` file in the project:

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
        # the default command to run wheneve the container is launched
        command: python manage.py runserver 0.0.0.0:80

This now provides a convenient way to run commands inside the Dockerised environment, and also gives us access to a
number of useful ``docker-compose`` commands. For example, you can use ``docker-compose build`` to build the entire
application, not just one image,


Create a new Django project in the application
-----------------------------------------------

For example, now we need to create a new Django project in the application (with ``django-admin startproject``), so we
can run:

..  code-block:: bash

    docker-compose run web django-admin startproject myapp .

This starts up a container (``web``, which according to ``docker-compose.yml`` will be based on the ``Dockerfile`` in
the same directory) and executes the ``django-admin`` command inside it. The advantage of executing the command inside
the container is that the project thus created will have been created in exactly the same environment that it will
eventually run.

The command will add a new ``myapp`` directory and a ``manage.py`` file. Although they were created *inside* the
container, so you wouldn't normally be able to see them, the ``volumes`` directive in the ``docker-compose.yml`` file
maps ``/app`` to the host filesystem, so you can see them and edit them without having to be inside the Docker
environment yourself.


Start the local project
-------------------------

Start the project by running ``docker-compose up`` in the terminal::

    ➜  docker-compose up
    Starting tutorial-project_web_1 ... done
    Attaching to tutorial-project_web_1
    web_1  | Watching for file changes with StatReloader

Open the project in your web browser by visiting http://127.0.0.1:8000.

(You may notice above that although the the Django runserver is running on port 80, the project is accessible on port
8000. The ``docker-compose.yml`` configuration file is responsible for :ref:`this port-mapping
<docker-compose-web>`.)

If you amend or even just save any Python file in the Django project, the runserver will reload the Python modules and
restart.


Add a start-up instruction to the ``Dockerfile``
------------------------------------------------

Docker Compose is only used locally, not in our cloud deployments. Moreover, the Django runserver that we're using here
is fine for local development but unsuitable for use in production. For production, we will use `Uvicorn
<https://www.uvicorn.org>`_ (Uvicorn is an ASGI gateway server for Python).

Add:

..  code-block:: text

    uvicorn==0.11.8

to ``requirements.txt``. Every time you amend ``requirements.txt``, you will need to rebuild the image, because it
implies a change to it:

..  code-block:: bash

    docker-compose build

The Django project can be started with Uvicorn, with ``uvicorn --host=0.0.0.0 --port=80 myapp.asgi:application``. This
should be baked into the ``Dockerfile`` itself. To the end of the file, add:

..  code-block:: Dockerfile

    CMD uvicorn --host=0.0.0.0 --port=80 myapp.asgi:application

Rebuild once more. Now when the web container is launched it will run ``uvicorn --host=0.0.0.0 --port=80
myapp.asgi:application`` automatically, to start it up in - for example - a cloud deployment.

However, when we start it locally with ``docker-compose up``, the ``command`` line in the ``docker-compose.yml`` file
will override that, and use ``python manage.py runserver 0.0.0.0:80`` instead.

If we need to run the project locally using Uvicorn rather than the runserver, we can do that by temporarily commenting
out the ``command`` line in the ``docker-compose.yml`` file.

Try it both ways. As before, the Django project can be found locally at http://127.0.0.1:8000.

..  admonition:: Static files when using Uvicorn

    The Django runserver provides a lot of convenience. An example is that it will (as long as ``DEBUG = True``)
    automatically serve static files such as CSS without additional configuration. When you launch the site using
    Uvicorn, or when ``DEBUG = False``, static files are not automatically served. You can try loading the `fonts.css
    <http://127.0.0.1:8000/static/admin/css/fonts.css>`_ static file in each configuration to see this for yourself. We
    will refine this later.

    In the meantime, make sure you set ``DEBUG = True`` and restore the ``command`` line in the ``docker-compose.yml``
    file before continuing.


..  include:: includes/03-local-2-useful-commands.rst


..  code-block:: bash

    docker-compose run web python manage.py shell

which will open a Django shell in the ``web`` container.


..  include:: includes/03-local-3-next.rst
