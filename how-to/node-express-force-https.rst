.. _how-to-express-js-https:

How to force HTTPS with Express.js
===================================================================

In order to ensure secure communication with users of your Express.js applications, you can make all traffic to use
HTTPS, by forcing a re-direct from HTTP.

An Express-based application on is always accessed through a reverse proxy. When a user makes a request to your
application, the reverse proxy interacts with your application on behalf of the client. For more on this topic, see the
`Express.js documentation <https://expressjs.com/en/guide/behind-proxies.html>`_.

We need to inform Express that its is behind a proxy. Edit your application's ``server.js``, to add::

    app.enable('trust proxy')

This setting will populate the request object with extra information; we can then query the request to determine
whether it was made over HTTP or HTTPS. Add the following prior to your other routing (you will need to modify this to
suit your application)::

    app.use(function(request, response, next) {

        if (process.env.NODE_ENV != 'development' && !request.secure) {
           return response.redirect("https://" + request.headers.host + request.url);
        }
        
        next();
    })

This will redirect all non-HTTPS requests.


Working locally
---------------

When working locally, you won't want this behaviour enabled. The best way to control it is via an environment variable,
that you read into ``server.js`` appropriately.
