.. _knowledge-security-policy:

Security
=================

This document provides an outline of the security policies and standards we adhere to.

..  note::

    This document does not describe all details. Some information will only be shared with other parties on the basis of
    a non-disclosure agreement, and we reserve the right to not to share any information that could compromise the
    security of our platform or our customers's websites.


Technology
----------

Divio is built using `Django <https://www.djangoproject.com/>`_, the `Python <https://www.python.org/>`_-based web
application framework.

Python
~~~~~~

Python is a language with strict security standards and policies. Python and modules in its standard libraries are
subject to very close scrutiny. Vulnerabilities are rare and dealt with promptly.


Django
~~~~~~

Django inherits Python’s advantages and builds on them. Over the years it has earned a particularly strong reputation
for very high security standards, thanks to the quality of its codebase and the policies it has adopted.

Django provides robust security out-of-the box. Core components and tools such as its authorisation framework,
permissions framework and templating language have been tried, tested, hardened and improved, on a vast scale, over many
years.

Django also configures security into its projects by default, and encourages good security by making it easier to do
things the secure way.


Pre-public Django security patches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a trusted, large-scale host of Django projects, we receive advance notification from the Django Project about
security releases, which means that we are able to have security patches in place before vulnerabilities are made
public.


Divio architecture
~~~~~~~~~~~~~~~~~~

A project's web application containers and database are not directly accessible outside our network.

All traffic to our sites are directed through our Load Balancers, before reaching the application runners that
orchestrate users' containerised applications.

All levels are redundant, including PostgreSQL clusters and cloud media storage instances.

All connections are encrypted, even within our architecture.


Divio security monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~

We monitor and log activity within and into our systems, and use automated systems to alert our infrastructure team to
unusual traffic or behaviour.

Details of these systems are not disclosed to other parties.


Third-party services
~~~~~~~~~~~~~~~~~~~~

Divio makes use of known services, such as the well-protected AWS and MS Azure stacks, that enjoy an international
reputation for robustness.

Details of other providers can be supplied on application, under the terms of a non-disclosure agreement.


Security options for Divio users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We’re able to add further protection for our users for their projects. For example, we offer:

* free SSL certificates to all customers and HTTPS by default
* offer security patches and layers, proactively, in response to significant CVEs
* CloudFlare DDoS protection

amongst other benefits.


Containerisation
~~~~~~~~~~~~~~~~

Divio uses Docker-based containerisation for deployment, which contributes extra layers of security to our
infrastructure.

Containerisation isolates running instances from each other. A vulnerability or even a breach affecting one site remains
isolated to that particular instance.

Our containerised architecture makes it very easy to apply important software patches and updates. Fresh containers can
be deployed to replace ones running outdated software without missing a beat, and we can apply updates - even major
updates - to parts of the infrastructure without disrupting services. Similarly, updates can be applied to users'
projects without any disruption to service.

Finally, the portability of Docker containers means that users’ websites, already safely isolated from the machines and
systems that host them, can be moved away very quickly should the hosting system suffer an attack or a breach. Users
applications will never be tied down to a compromised infrastructure.


Backups
~~~~~~~

Backups are executed automatically as well as on-demand, stored separately and encrypted.


Policies
--------

General code security and integrity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We adopt industry best-practices for security both in our own infrastructure and the projects we host for our users.

We use well-tested security libraries and do not create our own. We never bypass built-in protections offered by our
technology stack, and make full use of them.

Staff security policy
~~~~~~~~~~~~~~~~~~~~~

Divio maintains a formal internal security policy, with which all staff are familiar. This covers such fundamental
topics as multi-factor authorisation, reporting, recording, online accounts, handling of physical devices and so on.

Some details of our staff security policy can be supplied on application, under the terms of a non-disclosure agreement.


Incident response plan
~~~~~~~~~~~~~~~~~~~~~~

Divio maintains a formal Incident response plan, governing incidents are recorded, escalated, dealt with and
followed-up.


Security report handling
~~~~~~~~~~~~~~~~~~~~~~~~

We have a dedicated security team, and encourage responsible reporting by providing dedicated and clearly advertised
security contact details. We take all reports seriously and respond to them promptly.


Security testing
~~~~~~~~~~~~~~~~

We regularly run security tests against our own software and infrastructure. This includes penetration tests run by
expert third-party security organisations.

Some details of our testing regime and its results can be supplied on application, under the terms of a non-disclosure
agreement.


Standards
---------

We are implementing the ISAE 3402 assurance standard, that allows us to demonstrate good security practices are in
place and operating effectively. ISAE 3402 is a newer mechanism for assurance, with wider scope, that evaluates
practices in a real-world context.

Our implementation of ISAE 3402 meets the requirements of clients with very strict demands in the banking sector that
use the Divio platform.


GDPR
~~~~

We are in compliance with the `European Union's General Data Protection Regulation
<https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679>`_.
