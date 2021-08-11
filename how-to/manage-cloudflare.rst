.. _how-to-manage-cloudflare-cache:

How to clear the Cloudflare cache
==================================

If your project uses Cloudflare CDN, you can clear it as required via our control panel.

.. note::

    This is only available if:

    * your project uses Cloudflare's CDN
    * the Cloudflare CDN was set up by Divio, and not independently

To clear the cache for a domain on your project, go to its *Domains* view and select the domain for which you need to clear the cache.

The cache will be cleared within a few minutes, and you will see a success message in the dashboard.

.. note::

    Cache-clearing is performed on domains, and applies to all other sub-domains under the same domain.

    For example, if you choose to clear the cache on *www.example.com* or *example.com* , it will apply to both of those
    domains, as well as *support.example.com*, *resources.example.com* and so on.

    However, it will not apply to *example.it*  or any other domains.

    It will not automatically apply to media files, unless these are also served from the same domain.
