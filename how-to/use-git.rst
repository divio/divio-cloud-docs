.. _use-git-manage-project:

How to use Git to manage your project
=====================================

Your Divio project is a Git repository, offering several advantages to the developer -
fine-grained revision control, excellent collaboration options, easy export and replication.

The :ref:`Divio app <divio-app>`, our desktop application for project management, also uses
Git behind the scenes for its *Upload* and *Download* operations.

.. image:: /images/upload-download.png
   :alt: 'Upload and download buttons in the Divio app'

If you are familiar with Git, then all you need to know is that your project is a completely
standard Git repository, and:

* our own Git server is ``git.divio.com``, but you can also :ref:`configure an external Git service for your project
  <configure-version-control>`
* by default, we use the branch ``develop`` (optionally, different Git branches can be linked to
  your Test and Live servers)

If you use the Divio app or the :ref:`Divio Shell <divio-shell>`, SSH keys to our Git server will be set up for you;
otherwise you will need to :ref:`set them up yourself <add-public-key>`.


Basic Git operations
--------------------

It's beyond the scope of this documentation to provide a guide to Git, but to get you started,
the basic operations you will need are described here.


Push your changes to the Cloud
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have made some local changes and want to push (i.e. upload) them to the Cloud, the basic
steps you need are:

* ``git status`` to see the changed files
* ``git add <file1> <file2>`` (etc) to stage the changes (alternatively, you can do ``git add .``
  to stage everything)
* ``git status`` to make sure everything has been staged
* ``git commit -m "<your commit message>"`` to commit the changes (provide a meaningful message for
  your own benefit)
* ``git push origin develop`` to push your local changes to the ``origin`` (i.e. our server)


Pull changes from the Cloud
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``git pull`` will pull fetch and merge any changes that have been made on the Cloud


Excluded directories
--------------------

Note that a number of directories and files are excluded (using the ``.gitgignore`` file) from the project. They include:

* ``.env`` - the project's virtualenv, for software installed using  pip
* ``data`` - temporary file storage
* ``static_collected`` - processed static files
* ``node_modules`` - for frontend frameworks
* ``.env-local``
