.. _how-to-duplicate-project:

How to duplicate a project
==========================

To help you re-use work and speed up your workflow, Divio offers two options for project duplication - Fork
and Mirror.

You might want to duplicate a project for a number of reasons, for example:

* to explore radical changes or development that you don't want to do on the original
* to prepare the launch of site-wide development or content changes, without disturbing the original
* to punch out a completely new project, based on an original
* to provide team members or clients with an exact copy of a project for training purposes


.. _how-to-duplicate-project-options:

Select your duplication option
------------------------------

To duplicate a project, select *Duplicate* from the project's options menu, in the organisation view:

.. image:: /images/guides/options-menu-organisations-view.png
   :alt: 'options menu'
   :width: 685

or in the project view:

.. image:: /images/guides/options-menu-project-view.png
   :alt: 'options menu'
   :width: 690

You need to give the duplicate a name, and decide whether to duplicate the project to the same organisation or a
different organisation.

Select the appropriate duplication action: *Fork* or *Mirror*.

.. _duplication-types:

Duplication types
~~~~~~~~~~~~~~~~~~~


Fork
^^^^

A fork is a form of duplication in which the new project will be an exact but independent copy of the original. A fork
will include the original’s code, database content, media, environment variables and all branches,  and retains the Git
history in its codebase. 

A fork is therefore useful when you want to undertake substantial new development, as it allows you to merge back
changes from the duplicate into the original using Git.



Mirror
^^^^^^

A mirror, unlike a fork, is dependent on the original it is created from. A mirror shares its codebase with
the original.  Whatever changes made to the codebase of the original will also be applied to each mirror.

Mirrors are useful when you have a large number of franchise-type sites that share exactly the same functionality.
Rather than needing to make, test and deploy the same changes hundreds of times, the mirror functionality allows you to
do this just once, on the original, and then deploy the changes to all the mirrors.


Select subscription options
---------------------------

After creating the duplicate, you will need to select a suitable subscription.
