..  admonition:: Local file storage is not a suitable option

    Your code may expect, by default, to be able to write and read files from local file storage (i.e. files in the
    same file-space as belonging to the application).

    **This will not work well on Divio** or any similar platform. Our stateless containerised application model does
    not provide persistent file storage. Instead, your code should expect to use a dedicated file storage; we provide
    AWS S3 and MS Azure blob storage options.
