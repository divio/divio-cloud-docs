..  _uwsgi-configuration:

uWSGI configuration
-------------------

Available environment variables:

``UWSGI_BUFFER_SIZE`` (default value: 4096)
    If your site has to deal with very large request headers, you may receive ``web invalid request
    block size`` error. In this case, you can increase the buffer size to allow larger request
    headers.
