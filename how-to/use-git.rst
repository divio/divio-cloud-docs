.. _use-git-manage-project:

How to use Git with a Divio application
=======================================

Your Divio application is a Git repository, offering several advantages to the developer -
fine-grained revision control, excellent collaboration options, easy export and replication.

We provide Git hosting by default. Our server is ``git.divio.com``. You can also :ref:`use an external Git provider
<configure-version-control>`.

By default, we use the branch ``develop``, but you can specify the Git branches to be used by each environment.

You will need to :ref:`set up your public key on our Control Panel <add-public-key>` if you use our Git server.


Important limitations
---------------------

Git repository contents
~~~~~~~~~~~~~~~~~~~~~~~~

Certain conditions can cause deployment errors when the Control Panel tries to read the Git repository. These will
typically appear in the deployment log with an exception from ``pygit2``, such as::

    Traceback (most recent call last):
      [...]
      File "/usr/local/lib/python3.6/site-packages/pygit2/repository.py", line 131, in __getitem__
        raise KeyError(key)
    KeyError: abaddeed2d00ad47a9bb82db969707a21dead81ed

This can be caused by:

* an empty directory committed to the repository (remove it or add a file to it)
* a `Git submodule included in the repository <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`_ (remove it)
* files containing mixed line endings, if the ``.gitattributes`` configuration includes an instruction to resolve them
  (remove ``* text=auto`` if it appears in ``.gitattributes``).


Git repository size
---------------------------

We don't impose limits on the size of your application's Git repository. However, as its size increases, both our
infrastructure and Git itself have to work harder to manage it.

Above 100MB for its Git repository, we cannot guarantee that an application will function smoothly,
especially when our platform is under heavy load. It can cause:

* slower deployments
* deployment timeouts
* long backup times

If your application's Git repository, including its history, exceeds 800 MB you are likely to run into persistent
deployment problems.

If you need to store large amounts of data, use the application's media storage rather than Git.


Basic Git operations
--------------------

It's beyond the scope of this documentation to provide a guide to Git, but to get you started,
the basic operations you will need are described here.


Push your changes to the Cloud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``git pull`` will pull fetch and merge any changes that have been made on the Cloud

