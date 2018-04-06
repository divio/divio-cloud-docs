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
      background: #b9b9b9;
    }

    /* ----- interactive debugger ----- */

    dl.question dt:before {font-family: FontAwesome; content: "\f059"; color: #FFB400; margin-right: 1em;}
    dl.question li:after {font-family: FontAwesome; content: " \f0a9"; color: #FFB400;}
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

How to debug Cloud deployment problems
==============================================================

Start with the :ref:`debugging checklist <debug-checklist>`. Work through the checklist by selecting the most
appropriate answer for each question until you arrive at a probable fault for the symptoms you're seeing.

There is also a :ref:`complete decision tree <debug-decision-tree>` for the debugging process.


Debugging checklist
---------------------------

..  rst-class:: debugging-checklist

..  rst-class:: step current-step

.. _debug-checklist:

Deployment on the Cloud has not worked as expected
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  rst-class:: question

Does the Control Panel show a "Last deployment failed" message?
    * :ref:`debug-cp-deployment-failed`
    * :ref:`The Control Panel does not show a Last deployment failed message
      <debug-cp-deployment-not-failed>`


.. _debug-cp-deployment-failed:
..  rst-class:: step

The Control Panel shows a *Last deployment failed* message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open the log. The relevant section will be towards the end, so work backwards from the end. Any error will be clearly
stated.

..  rst-class:: question

What does the log contain?
    * :ref:`The deployment log appears to be empty <debug-cp-deployment-failed-deployment-log-empty>`
    * :ref:`The deployment log appers to contain no errors <debug-cp-deployment-failed-deployment-log-no-error>`
    * :ref:`The deployment log refers to an error <debug-cp-deployment-failed-deployment-log-error>`

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-failed-deployment-log-empty:
..  rst-class:: probable-fault step fas fa-exclamation-triangle

Probable fault: temporary problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please try again. This is a rare and usually temporary problem. You may need to wait a few minutes for the
condition to clear. If the issue is urgent, or you have already tried again, please contact Divio Support.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-failed-deployment-log-no-error:
..  rst-class:: step

The deployment log contains no obvious error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check the site's *runtime logs* (via the *Logs* menu).

..  rst-class:: question

Do you see any clear errors in the logs for the ``web`` container (of the appropriate server, Test or Live)?
    * :ref:`The runtime log contains errors <debug-cp-deployment-failed-deployment-log-no-error-runtime-log-error>`
    * :ref:`The runtime log contains no obvious error
      <debug-cp-deployment-failed-deployment-log-no-error-runtime-log-no-error>`

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-failed-deployment-log-no-error-runtime-log-no-error:
..  rst-class:: probable-fault step

Probable fault: application is too slow to start and times out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Probably your application took so long to start up that it triggered a timeout condition. On
our platform, if a site is not up and running within a certain period after its build has
completed, then the deployment is marked as failed.

This could happen because it is waiting for another external resource to become available, or the
processing it needs to do at start-up is excessive. These issues generally represent a programming
problem that needs to be resolved.

Build the site locally and start up the application to investigate why it is taking so long.

If the start-up processes can't be made faster or more lightweight, investigate an asynchronous
processing option such as :ref:`celery` to allow them to go on in the background while the project
starts up.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-failed-deployment-log-no-error-runtime-log-error:
..  rst-class:: probable-fault step

Probable fault: programming error in runtime code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Probably the issue is a programming error in the site that takes down Django as it launches (typically, this will
be an ``ImportError``). The runtime log will reveal the error.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-failed-deployment-log-error:
..  rst-class:: step

The deployment log contains an error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The end of the log will contain the key error.

..  rst-class:: question

What does the error most closely resemble?
    * :ref:`Could not find a version that matches [...]
      <debug-cp-deployment-failed-deployment-log-error-dependency-conflict>`
    * :ref:`npm ERR! [...] ERR! /npm-debug.log <debug-cp-deployment-failed-deployment-log-error-npm-error>`
    * :ref:`ImportError <debug-cp-deployment-failed-deployment-log-error-import-error>`
    * :ref:`ReadTimeoutError <debug-cp-deployment-failed-deployment-log-error-timeout>`
    * :ref:`The error does not seem to be any of the above <debug-cp-deployment-failed-deployment-log-error-other-error>`

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-failed-deployment-log-error-dependency-conflict:
..  rst-class:: probable-fault step

Probable fault: dependency conflict
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An error that starts::

    Could not find a version that matches [...]

indicates that two or more of the components in your system have specified incompatible Python dependencies.

See :ref:`debug-dependency-conflict`.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-failed-deployment-log-error-npm-error:
..  rst-class:: probable-fault step

Probable fault: A Node error has halted the build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example::

    npm ERR! There is likely additional logging output above.
    [0m[91m
    [0m[91mnpm[0m[91m ERR![0m[91m Please include the following file with any support request:
    [0m[91mnpm ERR! /npm-debug.log
    [0m

In this case one of the Node component installation processes has failed. If the error is not clear from the log,
contact Divio support for advice.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-failed-deployment-log-error-import-error:
..  rst-class:: probable-fault step

Probable fault: An import error halts one of the site build routines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example::

    Step 8/8 : RUN DJANGO_MODE=build python manage.py collectstatic --noinput
    [...]
    ImportError: No module named django_select2

In this case a Python application launched by an instruction in the ``Dockerfile`` has caused Django to halt with an
error while it was trying to run the ``collectstatic`` command. This is a programming error. The traceback will show
where it occurred.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-failed-deployment-log-error-timeout:
..  rst-class:: probable-fault step

Probable fault: temporary timeout error (read timeout)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example::

    ReadTimeoutError: [...] Read timed out.

This may occasionally occur when our deployment infrastructure is under heavy load. In most cases you can simply try
again. If the issue is urgent, or you have already tried again, please contact Divio Support.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-failed-deployment-log-error-other-error:
..  rst-class:: probable-fault step

Probable fault: A runtime error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are not sure what the error message reveals, please contact Divio support for assistance.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


.. _debug-cp-deployment-not-failed:
..  rst-class:: probable-fault step

Probable fault: programming error at runtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes there is no failed deployment log, but the site fails to start. This is typically caused
by a programming error that becomes apparent at runtime.

Usually, the browser will show a Django traceback, if the site is in ``DEBUG`` mode (this is the default for the *Test*
server). Under some circumstances, it might not, but the error will be shown in the site's runtime logs, available from
the *Logs* menu in the Control Panel.

..  rst-class:: restart-link

:ref:`Restart the checklist <debug-checklist>`


..  _debug-decision-tree:
..  rst-class:: debug-decision-tree

Decision tree
-------------

This tree represents the logic of the debugging checklist.

* :ref:`Deployment on the Cloud has not worked as expected <debug-checklist>`:

  * :ref:`debug-cp-deployment-failed`

    * The deployment log appears to be empty: :ref:`debug-cp-deployment-failed-deployment-log-empty`
    * :ref:`debug-cp-deployment-failed-deployment-log-no-error`

      * Runtime log contains no errors: :ref:`debug-cp-deployment-failed-deployment-log-no-error-runtime-log-no-error`
      * Runtime log contains errors: :ref:`debug-cp-deployment-failed-deployment-log-no-error-runtime-log-error`

    * :ref:`debug-cp-deployment-failed-deployment-log-error`

      * ``Could not find a version that matches [...]``:
        :ref:`debug-cp-deployment-failed-deployment-log-error-dependency-conflict`
      * ``npm ERR! [...] ERR! /npm-debug.log``: :ref:`debug-cp-deployment-failed-deployment-log-error-npm-error`
      * ``ImportError``: :ref:`debug-cp-deployment-failed-deployment-log-error-import-error`
      * ``ReadTimeoutError``: :ref:`debug-cp-deployment-failed-deployment-log-error-timeout`
      *  An error not listed above: :ref:`debug-cp-deployment-failed-deployment-log-error-other-error`

  * The Control Panel does not show a *Last deployment failed* message: :ref:`debug-cp-deployment-not-failed`
