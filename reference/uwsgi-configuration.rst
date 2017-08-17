..  _uwsgi-configuration:

uWSGI configuration
-------------------

uWSGI offers `a vast number of configuration variables <http://uwsgi-docs.readthedocs.io/en/latest/Options.html>`_.

Any one of them can be set using an enviroment variable starting ``UWSGI_``, followed by the name of the
variable in uppercase.

For example, the ``processes`` variable can be set by setting ``UWSGI_PROCESSES``.

Generally you will not need to touch these variables, and we recommend leaving them alone unless you need to change
something and you know what you are doing.

Some that you are more likely to need to adjust include:

``UWSGI_BUFFER_SIZE``
    (default value: ``4096``) If your site has to deal with very large request headers, you may receive a ``web
    invalid request block size`` error in your project's logs.

    In this case, you can increase the buffer size to allow larger request headers. (You may also want to find out
    why your site is running into such large request headers - for example, its cookies may be excessively large.)
