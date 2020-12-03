.. _cron-jobs:

Cron jobs
===============================

Cron jobs are available from the *Cron Jobs* view in the Control Panel. Note that cron jobs are not available on all
project plans.


Creating tasks
--------------

When adding a cron job, you need to provide the command that will be executed, and the period according to which the
task should be run.

For example, if you select every 10 minutes, the task will be run every hour at :10, :20, :30, :40, :50 and :00.

A cron job can execute a simple command (for example: ``/usr/local/bin/python manage.py cms fix_tree``) or a script.

After adding or changing a cron job, the environment will need to be redeployed for the cron configuration to be
applied.


Cron commands
~~~~~~~~~~~~~~~~~~~~

Cron does not provide a fully-fledged environment - it's not a bash environment, for example, and commands that include
bash syntax will not work. It can only execute *commands*.

Moreover, to avoid ambiguity and expected results, it is wise to be explicit. For example, in the Python example above,
we specified the full Python path::

    /usr/local/bin/python


Cron job timeouts
-----------------

We apply a default timeout of ten minutes on processes started by cron jobs. Longer-running processes should be handled
by a more appropriate task manager (such as Celery) instead.
