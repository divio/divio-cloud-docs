..  _environment-configuration:

Local environment configuration
===============================

Your local Divio set-up can be configured via the ``~/.aldryn`` file.

It contains a JSON dictionary, for example::

    {
        "update_check_timestamp": 1501185567,
        "skip_doctor_checks": [
            "docker-machine"
        ]
    }

The ``skip_doctor_checks`` are particularly useful, and can be used to disable certain automated
checks run by the Divio app and the :ref:`divio doctor <divio-doctor>` command (for example, if you
are working offline, or with network restrictions).

The checks that ``divio doctor`` runs are classes in `check_system.py
<https://github.com/divio/divio-cli/blob/master/divio_cli/check_system.py>`_. Add them to
the list in ``skip_doctor_checks`` to disable them:

``login``
    ``LoginCheck``

    Can we log in to the Control Panel?
``git``
    ``GitCheck``

    Is Git is installed locally?
``docker-client``
    ``DockerClientCheck``

    Is the ``docker`` command available?
``docker-machine``
    ``DockerMachineCheck``

    Is the ``docker-machine`` command available?
``docker-compose``
    ``DockerComposeCheck``

    Is the ``docker-compose`` command available?
``docker-server``
    ``DockerEngineCheck``

    Is the Docker daemon running, and can we connect to it?
``docker-server-ping``
    ``DockerEnginePingCheck``

    Does the Docker container have connectivity to the outside world? (Checks by running ``docker
    run --rm busybox sh -c "ping -c 1 -w 5 8.8.8.8"``.)
``docker-server-dns``
    ``DockerEngineDNSCheck``

    Does a Docker container have connectivity to the outside world? (Checks by running ``docker run
    --rm busybox sh -c "timeout -t 5 nslookup control.divio.com"``.)
