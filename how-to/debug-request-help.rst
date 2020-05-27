.. _debug-describe-problem:

How to get help when you have a problem
==========================================

In order to help Divio support help you, it's important to provide us with the information we need, and to be sure it's
:ref:`something that we can actually help you with <support-scope>`.

This page contains a :ref:`report template <problem-report-template>` and an :ref:`example of a good report
<problem-report-example>`.


Grant support access
----------------------

We will need you to grant support access to your account.
Please go to `your privacy settings <https://control.divio.com/account/change-privacy-settings/>`_,
and grant consent for Support Access.

Preferably, grant support for one year so that on future occasions we will not need to ask you again.
The access you grant will be used exclusively for support purposes within Divio.


Provide key information
------------------------

* The dashboard URL of each project - for each project you are referring to, we need its dashboard URL, in the form ``https://control.divio.com/control/...``.
* The precise steps to replicate your issue - we may need to be able to replicate your issue - what action(s) must we
  take to see it for ourselves? If there are multiple steps involved, please list them.
* What you expect to happen - we need to understand what you expected to happen. If you expected some output or result,
  describe it, bearing in mind that we may not be familiar with your project.
* What actually does happen - describe the unexpected output or result. Include logs, error messages from the server
  and browser and so on.
* Tell us what troubleshooting steps you have taken so far - please check:

  * Have you set up the project locally?
  * Does the issue present itself there?
  * If appropriate, test with your :ref:`local project in live configuration <local-in-live-mode>`.
  * Are you using logging to help understand the behaviour of the program?

  Include any relevant information from troubleshooting in your report.

.. _problem-report-template:

Template
--------

You may find it helpful to copy and paste this template into your support requests:

    **Dashboard URLs**

    * ``https://control.divio.com/control/...``

    **Steps to replicate**

    * step 1
    * step 2
    * step 3

    **What we expected to happen**

    [description]

    **What actually happened**

    [description]

    **Troubleshooting information**

    The issue [does/does not] occur when running the project locally in live configuration.

    **Additional information**

    [include error messages, links to logs, etc]


.. _problem-report-example:

Example report
--------------

A good report might look something like this:

    We are having problems with a form in our DynaCorp Global project
    https://control.divio.com/control/3097/edit/50704/. To see this:

    * log in at https://example.com/clientarea with the username "diviosupport" and password "T3mpP4sswd" that we have
      prepared for you
    * in the "Manage your holding" page at https://example.com/clientarea/holdings/edit, change
      the text in the "Name" field in the form that appears, and press "Update"

    At this point you should be redirected to https://example.com/clientarea/holdings, with the data you entered.

    Instead what actually happens is that sometimes the expected data will appear, but approximately 50% of the time,
    it will not.

    There are no errors in the logs or browser. The error occurs only on the Live server, not on Test or locally (even
    when running in Live configuration).

As well as giving us enough information to continue investigating further, the inclusion of information about where it
has been tested provides some valuable clues as to the nature of the problem.

Ensure that we have access to your project
------------------------------------------

If your project uses the Divio Git server, we'll be able to set it up locally for testing if we need to. However if you
:ref:`use a private remote Git repository <configure-version-control>`, this won't be possible unless you can provide
us with access to the repository. Usually we will provide you with :ref:`a public key to add to the respository
<git-setup-ssh>`.


.. _support-scope:

What we can and can't help with
--------------------------------

Our technical support is limited in scope to our platform and infrastructure:

* general questions about the use of the platform and its tools
* use and configuration of the local development environment
* best practices for project configuration on Divio
* best practices for project migration to Divio
* deployment issues related to our infrastructure

We are unable to provide support for:

* general questions about development
* debugging of user applications or third-party software
* users’ local hardware/software set-up

Please note that we are able to provide more in-depth technical support for Business-class projects than those on
Economy plans. For more information please see our `full support policy
<https://www.divio.com/terms-and-policies/support-policy/>`_.
