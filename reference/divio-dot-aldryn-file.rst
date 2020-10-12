..  _environment-configuration:

Divio CLI configuration
===========================

The behaviour of the Divio CLI can be managed via a JSON configuration file.


Location of the file
--------------------

The file is created by the CLI and will be found at either:

* ``~/.config/divio/config.json``, or
* ``~/.aldryn`` (the older location for the file - if this file exists it will take precedence)


File structure
--------------

It contains a JSON dictionary, for example::

    {
        "update_check_timestamp": 1501185567,
        "skip_doctor_checks": [
            "docker-server-dns"
        ]
    }


..  _skip-doctor-checks:

Using ``skip_doctor_checks``
----------------------------

The ``skip_doctor_checks`` are particularly useful, and can be used to disable certain automated
checks run by the Divio app and the :ref:`divio doctor <divio-doctor>` command (for example, if you
are working offline, or with network restrictions).

A common need is to disable a check that fails for some reason, in circumstances when you know that the failure is
not relevant in the context of your environ,

The checks that ``divio doctor`` runs are classes in `check_system.py
<https://github.com/divio/divio-cli/blob/master/divio_cli/check_system.py>`_. If a check fails that you think can be
ignored, add it to the list in ``skip_doctor_checks`` to disable it, as in the example above.

``login``
    ``LoginCheck``

    Checks that the CLI can connect to the endpoint on the Divio Control Panel.
``git``
    ``GitCheck``

    Checks that Git is installed by running ``git --version``.
``docker-client``
    ``DockerClientCheck``

    Checks that the Docker client is available by running ``docker --version``.
``docker-compose``
    ``DockerComposeCheck``

    Checks that Docker Compose is available by running ``docker-compose --version``.
``docker-server``
    ``DockerEngineCheck``

    Checks that a command can be executed in a container by running ``docker run --rm busybox``.
``docker-server-ping``
    ``DockerEnginePingCheck``

    Checks that a Docker container has connectivity to the Internet by running ``docker
    run --rm busybox sh -c "ping -c 1 -w 5 8.8.8.8"``.
``docker-server-dns``
    ``DockerEngineDNSCheck``

    Checks that a Docker container can resolve DNS queries by running ``docker run --rm busybox sh -c "timeout 5
    nslookup -type=a control.divio.com. || timeout -t 5 nslookup -type=a control.divio.com."``
