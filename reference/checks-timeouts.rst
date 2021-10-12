.. _checks-timeouts:

Checks, limits and timeouts on the Divio platform
=================================================

Various processes and operations on our platform are subject to checks, timeouts and limits.
Knowing what these are can help pin-point problems experienced when building or running applications.


.. _checks-timeouts-deployment:

Deployment health-checks
------------------------

The deployment process must complete :ref:`each stage of its operations <deployment-steps>` successfully within a given
time. If any of these checks fail, the deployment itself will fail.

* :ref:`Docker build stage <deployment-build>`; will time out with a failure if not completed within 30 minutes.
* :ref:`Release commands stage <deployment-release-commands>`; each command will time out with a failure if not
  completed within 30 minutes.
* :ref:`Scaling <deployment-scaling>`: each container must return a positive HTTP response to our application
  controller within 20 seconds of establishing a connection. The application controller will repeat this test at
  intervals, for up to 60 seconds.

When a deployment copies data from another environment, the copy operation will time out with a failure if not
completed within 30 minutes.


.. _checks-timeouts-runtime:

Run-time limits
---------------

.. _checks-timeouts-requests:

Request timeouts
~~~~~~~~~~~~~~~~~

Traffic reaches customer applications via our load-balancers.

* *connection*: the load-balancer connects to the one of the application's containers; if a handshake is not completed
  within 5 seconds, it will try to connect to another container, if one is available
* *send*: the load-balancer sends a request to an application; if this does not complete successfully within 10
  seconds, it will try to connect to another container, if one is available
* *read*: after delivering a request to the application, the load-balancer must receive a response within 30 seconds;
  this is also the maximum allowed time between responses in case of chunked transfers

If any of these time limits are exceeded, the load-balancer will report a HTTP 504 *Gateway timeout*.

If the connection and send phases do not complete successfully within a total of 15 seconds, the load-balancer will
report a HTTP 502 *Application not responding error* and will not attempt to connect to any remaining containers.

In almost all cases, these errors are caused by a fault in the application, and its run-time logs will provide clues
as to its nature.


Request sizes
~~~~~~~~~~~~~

* maximum request header size: determined by the application itself
* maximum request body size: 500MB; imposed by our load-balancer


Other limits
~~~~~~~~~~~~

* concurrent database connections per environment: limited to 60
* requests to Elasticsearch clusters: if the Elasticsearch load-balancer does not receive a response within within 120
  seconds it will issue an HTTP 504 ``Gateway timeout``


Operations
-----------

Divio CLI database and media push and pull
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* limited to 2GB - in practice, keeping transfer size below 500MB is strongly recommended; for larger media transfers,
  :ref:`use an S3 client<interact-storage>`
* terminated after 30 minutes
