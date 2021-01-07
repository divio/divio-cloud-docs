Divio developer handbook
==============================


..  rst-class:: column


:ref:`Get started <introduction>`
-------------------------------------------------------

**Tutorials.** A hands-on introduction to Divio for developers. *Recommended for all new users.*


..  rst-class:: column


:ref:`How-to guides <how-to>`
-------------------------------------------------------

**Step-by-step guides.** Covers key tasks and operations and common problems.


..  rst-class:: column clearfix

:ref:`Background <background>`
-------------------------------------------------------

**Explanation.** Clarification and discussion of key topics.


..  rst-class:: column

:ref:`Reference <reference>`
-------------------------------------------------------

**Technical reference.** Covers tools, components, commands and resources.


..  rst-class:: clearfix row

Additional resources
--------------------

..  rst-class:: column

..  raw:: html

    <h3 class="mt-0">Divio Community Slack</h3>

    <p>The Divio Community Slack group is for all Divio users.</p>

    <a class="btn btn-primary btn-small" target="_blank" href="https://join.slack.com/t/divio-community/shared_invite/zt-k5h56uqa-fPxLJq5vQx2OQ9xTiSJnoQ" role="button">Join the Divio Community Slack group</a>

    <p>&nbsp;</p>

..  rst-class:: column

..  raw:: html

    <h3 class="mt-0">The Divio API</h3>

    <p>The Divio API is a powerful tool for interacting with our infrastructure and your projects. See:</p>

    <ul>
        <li><a href="/how-to/use-api/#use-divio-api">How to use the Divio API</a> in this documentation</li>
        <li><a href="https://api.docs.divio.com">Divio API reference documentation</a></li>
    </ul>


About the Divio cloud deployment platform
-----------------------------------------

`Divio <https://divio.com>`_ is a platform for containerised web
projects. Divio's cloud platform aims to offer developers:

**More reliable deployment** - it's built in Python and Django, and uses Docker
to give application developers a local development environment that is
consistent between the Cloud live and test servers - in other words, a system
where if it works on your machine, you can expect it to work in production.

**Easier deployment and maintenance** - the Dockerised Cloud platform makes it
possible for developers to get their projects online, and to take charge of
deployment, maintenance and scaling, without needing the operations or system
administrator skills this usually demands to do well.

**Better portability** - the containerisation technology used in Divio
projects guarantees portability and means freedom from lock-in to a single
provider. A Divio project can be easily deployed on another platform
that supports Docker.


.. toctree::
    :hidden:

    introduction/index
    how-to/index
    reference/index
    background/index
