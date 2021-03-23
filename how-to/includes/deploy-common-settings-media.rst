Media
~~~~~~~~~~~

If your application needs to handle generated or user-uploaded media, it should use a media object store.

Media credentials are provided in ``DEFAULT_STORAGE_DSN``. See :ref:`how to parse the storage DNS
<interact-storage-parse-DSN>` to obtain the credentials for the media object stores we provide. Your application needs
to be able to use these credentials to configure its storage.

When working in the local environment, it's convenient to use local file storage instead (which can be also be
configured using a variable provided by the local environment).

Modern application frameworks such as Django make it straightforward to configure an application to use storage on
multiple different backends, and are supported by mature libraries that will let you use a Divio-provided S3 or MS
Azure storage service as well as local file storage.
