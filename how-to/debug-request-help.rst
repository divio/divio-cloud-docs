.. _debug-describe-problem:

How to describe a problem when contacting Divio support
==============================================================

In order to help Divio support help you, it's important to provide us with the information we need, and to be sure it's
:ref:`something that we can actually help you with <support-scope>`.


What information we need
------------------------

* The dashboard URL of each project - for each project you are referring to, we need its dashboard URL, in the form ``https://control.divio.com/control/...``.
* The precise steps to replicate your issue - we may need to be able to replicate your issue - what action(s) must we
  take to see it for ourselves? If there are multiple steps involved, please list them.
* What you expect to happen - we need to understand what you expected to happen. If you expected some output or result,
  describe it, bearing in mind that we may not be familiar with your project.
* What actually does happen - sescribe the unexpected output or result. Include logs, error messages from the server
  and browser and so on.
* Tell us what troubleshooting steps you have taken so far - please check:

  * Have you set up the project locally?
  * Does the issue present itself there?
  * If appropriate, test with your local project in live configuration.
  * Are you using logging to help understand the behaviour of the program?

  Include any relevant information from troubleshooting in your report.


Example report
--------------

A good report could look something like this:

    We are having problems with a form in our DynaCorp Global project
    https://control.divio.com/control/3097/edit/50704/. To see this:

    * log in at https://example.com/clientarea with the username "diviosupport" and password "t3mpp4sswd" that we have
      prepared for you
    * in the "Manage your holding" page at https://example.com/clientarea/holdings/edit, change
      the text in the "Name" field in the form that appears, and press "Update"

    At this point you should be redirected to https://example.com/clientarea/holdings, with the data you entered.

    Instead what actually happens is that sometimes the expected data will appear, but approximately 50% of the time,
    it will not be.

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

* general questions about use of the platform and its tools
* use and configuration of the local development environment
* best practices for project configuration on Divio Cloud
* best practices for project migration to Divio Cloud
* deployment issues related to our infrastructure

We are unable to provide support for:

* general questions about development
* debugging of user applications or third-party software
* users’ local hardware/software set-up

Please note that we are able to proide more in-depth technical support for Business-class projects than those on
Economy plans. For more information please see our `full support policy
<https://www.divio.com/terms-and-policies/support-policy/>`_.
