.. raw:: html

    <style>

    /* ----- decision tree ----- */

    .debug-decision-tree li {
      margin-left: 1em;
      padding-left: 1em;
      position: relative;
      list-style: none !important;
    }

    .debug-decision-tree li li {
      margin-left: 0;
    }

    .debug-decision-tree li::after {
      content:'';
      position: absolute;
      top: 0px;
      bottom: -10px;
      left: -5px;
      width: 2px;
      background: #b9b9b9;
    }
    .debug-decision-tree li:last-child::after {
      content:'';
      display: none;
    }
    .debug-decision-tree li::before {
      content:'';
      position: absolute;
      top: 10px;
      left: -5px;
      width: 13px;
      height: 2px;
      background: #b9b9b9;a=
    }

    /* ----- interactive debugger ----- */

    .rst-content dl.question dt {background: none; border: none; color: black;}
    .rst-content dl.question dt:before {font-family: FontAwesome; content: "\f059"; color: #FFB400; margin-right: 1em;}
    .rst-content dl.question li a:after {font-family: FontAwesome; content: " \f0a9"; color: #FFB400;}
    .rst-content dl.question dd ul li {list-style: none;}
    .probable-fault h3::before {font-family: FontAwesome; content: "\f071"; color: #ffb400; margin-right: 1em;}

    div.step {
      border: 1px solid black;
      padding: 20px;
      margin: 2em 0 2em;
      border-radius: 10px;
      background: #eeeeee;
      /* by default, hide each step in the process */
      display: none;
      }

    /* but display it if it is actually selected */

    div.current-step {
      display: block;
    }

    .restart-link {text-align: right;}
    .restart-link:after {font-family: FontAwesome; content: " \f021"; color: red;}
    </style>

    <script>
    window.addEventListener('load', function () {
        $('.debugging-checklist .internal, .debug-decision-tree .internal').on('click', function (e) {
            e.preventDefault();

            var $this = $(this);
            var anchor = $this.attr('href');
            var step = $(anchor).parent();

            if (step.length && !step.is('current-step')) {
                $('.current-step').removeClass('current-step');
                step.addClass('current-step');
                if (window.history.pushState) {
                  window.history.pushState('', {}, anchor);
                }
            }
        });

        if (window.location.hash) {
            $('.internal[href$="' + window.location.hash + '"]').trigger('click');
        }

        $(window).on('hashchange', function () {
            $('.internal[href$="' + window.location.hash + '"]').trigger('click');
        });
    });
    </script>

.. _debug-deployment-problems:

How to debug `Divio Cloud <https://www.divio.com>`_ deployment problems
=======================================================================

Start with the :ref:`debugging checklist <debug-checklist>`. Work through the checklist by selecting the most
appropriate answer for each question until you arrive at a probable fault for the symptoms you're seeing.

There is also a :ref:`complete decision tree <debug-decision-tree>` for the debugging process.


Debugging checklist
---------------------------

..  rst-class:: debugging-checklist
..  rst-class:: step current-step
..  _debug-checklist:

Start here: a deployment has not worked as expected
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  rst-class:: question

Does the environment pane show a "Last deployment failed" error message?
    * Yes, :ref:`the error message is shown <debug-deployment-error-shown>`
    * No, :ref:`the error message is not shown <debug-deployment-error-not-shown>`


..  _debug-deployment-error-shown:
..  rst-class:: step

The Control Panel shows a *Last deployment failed* message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open the *failed* link to see the deployment log. The relevant section will be towards the end, so work backwards from
the end. Any error will be clearly stated.

..  rst-class:: question

What does the deployment log contain?
    * :ref:`The log appears to be empty <debug-deployment-log-empty>`
    * :ref:`The log appears to contain no errors <debug-deployment-log-no-error>`
    * :ref:`The log refers to an error <debug-deployment-log-error>`

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


..  _debug-deployment-log-empty:
..  rst-class:: probable-fault step

Probable fault: temporary problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please try again. This is a rare and usually temporary problem. You may need to wait a few minutes for the
condition to clear.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-deployment-log-no-error:
..  rst-class:: step

The deployment log contains no obvious error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The build process succeeded without errors, creating an image and then releasing containers that passed the
all health-checks, but all the same, the site is not working as expected. This should not occur, but can do in
certain quite specific circumstances.

Check the environment's runtime logs.

..  rst-class:: question

Do you see any obvious errors in the runtime logs for the environment's ``web`` container?
    * Yes, :ref:`the runtime log contains errors <debug-runtime-log-error>`
    * No, :ref:`the runtime log contains no obvious error <debug-runtime-log-no-error>`

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-runtime-log-no-error:
..  rst-class:: probable-fault step

The runtime log contains no errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Either the application is failing to write error logs, or some other problem has occurred. Please contact Divio
Support.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-runtime-log-error:
..  rst-class:: probable-fault step

The runtime log contains errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The probable cause is a programming issue. The runtime logs should help you understand the nature of this problem.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-deployment-log-error:
..  rst-class:: step

The deployment log contains an error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The end of the log will generally contain the key error.

..  rst-class:: question

Is the error:
    * :ref:`Container error: unable to connect to the container <debug-container-error>`
    * :ref:`Could not find a version that matches <debug-python-version-error>`
    * :ref:`npm ERR! [...] ERR! /npm-debug.log <debug-npm-error>`
    * :ref:`ReadTimeoutError <debug-read-timeout-error>`

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-container-error:
..  rst-class:: probable-fault step

``Container error: unable to connect to the container``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will see something like::

    Trying to connect to internal container http://10.0.0.164:11453/ (0:00:59.666292 with 148 retries)...
    connection error.
    Unable to connect! Endpoint verification failed.

The load-balancer was unable to connect to each of the environment's newly-launched containers and obtain a positive
HTTP response within 20 seconds of making the connection. The environment's runtime logs will contain more
information about the problem. If the logs don't contain a traceback revealing a programming error, the most likely
issue is that the application was too slow to start up.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-python-version-error:
..  rst-class:: probable-fault step

``Could not find a version that matches [...]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python application, indicates that a specified dependency cannot be found - typically because two or more of the 
components in your system have specified incompatible Python dependencies.

    For Aldryn Django applications, see :ref:`debug-dependency-conflict`.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-npm-error:
..  rst-class:: probable-fault step

``npm ERR! [...] ERR! /npm-debug.log``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Probable fault: A Node error has halted the build.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-read-timeout-error:
..  rst-class:: probable-fault step

``ReadTimeoutError``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This may occasionally occur when our deployment infrastructure is under heavy load. In most cases you can simply
try again.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-deployment-error-not-shown:
..  rst-class:: probable-fault step

The environment does not show a "Last deployment failed" error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Probable fault: programming error at runtime

Sometimes there is no failed deployment log, but the site fails to start. This is very rare, and is typically
caused by a programming error that becomes apparent only at runtime, after basic health-checks have passed.

The error will be shown in the site’s runtime logs, available from the Logs menu in the Control Panel.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


..  _debug-decision-tree:
..  rst-class:: debug-decision-tree

Decision tree
-------------

This tree represents the logic of the debugging checklist.



* :ref:`Deployment on the Cloud has not worked as expected <debug-checklist>`:

  * :ref:`A "Last deployment failed" error message is shown <debug-deployment-error-shown>`

    * :ref:`The deployment log appears to be empty <debug-deployment-log-empty>`
    * :ref:`The deployment log appears to contain no errors <debug-deployment-log-no-error>`

      * :ref:`Runtime log contains no errors <debug-runtime-log-no-error>`
      * :ref:`Runtime log contains errors <debug-runtime-log-error>`

    * :ref:`The deployment log contains an error <debug-deployment-log-error>`

      * :ref:`Container error: unable to connect to the container <debug-container-error>`
      * :ref:`Could not find a version that matches [...] <debug-python-version-error>`
      * :ref:`npm ERR! [...] ERR! /npm-debug.log <debug-npm-error>`
      * :ref:`ReadTimeoutError <debug-read-timeout-error>`

  * :ref:`A "Last deployment failed" error message is not shown <debug-deployment-error-not-shown>`
