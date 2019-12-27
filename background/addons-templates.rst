.. _addon-templates:

Django addons and templates
============================

Templates at the project level will override templates at the
application level if they are on similar paths. This is standard Django behaviour,
allowing application developers to provide templates that can easily be
customised.


On initial project creation
---------------------------

For your convenience, when you first create a project, any templates in addons
are copied to the project level so you have them right at hand (*if* the addon's
:ref:`package name and inner application name match <addon_application_naming>`.)

For example, templates from Aldryn News & Blog will be copied to
``templates/aldryn_newsblog/`` in your project.

If a template does not exist in the project's ``templates`` directory, Django
will simply fall back to the one in the addon itself.


Subsequent addon updates
-------------------------

After templates have been copied to the project's ``templates`` directory, they
will not be copied again, so as not to overwrite any changes the project
developer may have made. However, this does mean that if an addon is
subsequently updated and its templates change, those changes will not appear in
your project.

In this case:

* if you have made changes to the templates in your project, you will need to
  obtain any updated templates and merge them with your own versions
* if you have not made any changes, you can simply delete your local versions
  and Django will use the updated application templates.
