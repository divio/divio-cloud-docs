.. _addons:

Addons
======

Aldryn Addons are Python/Django applications that have been packaged for easy deployment on Divio. 

.. note::
    In order to use *Aldryn addons* you need to use *Aldryn*. But you do not need to use *Aldryn* to install any
    applications in Divio. See :ref:`All about Aldryn <aldryn>`. Addons are additional extensions for your own
    convenience. 
 
An Aldryn addon wraps up a Python application such as django CMS, Django Filer or even Django itself so that it can be
:ref:`added to a Divio project via the web interface on our Control Panel <aldryn-addons>`. 

If you were to install an application by hand, say using *pip install* ... , you would then need to wire it up into a
project, ensuring that it is correctly configured and has appropriate settings. 

An addon can take care of all this for you, for example, even ensuring that ``MIDDLEWARE`` options it requires are
inserted in the correct order, and that its URL configurations are correctly added to the project.
 
``Settings`` can also be exposed to the user in a simple form on the Control Panel.
 
Packaging a Python application as an addon allows users to add it to their project even without having the technical
knowledge that would otherwise be required to do so, and allowing them to :ref:`update it to newer versions easily
<update-addon>` when they become available.
 
 
For more details, see our Developer Handbook on :ref:`what Aldryn addons are <aldryn>`.
