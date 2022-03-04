.. _diagnose-performance-issues:

How to diagnose performance problems
================================================

In a web applications, a performance problem is generally experienced in two ways: as a lack of speed in responding to
client requests, or unexpected errors from the site.

Errors caused by performance problems are typically (but not limited to) *Application not responding* or *Gateway timeout* errors.

..  important::

    **Almost without exception**, performance problems with sites running on Divio are caused by problems originating
    within the applications themselves, and are not related to the performance of our servers, network or
    infrastructure.

    We monitor all of our services around the clock. Any components whose performance or operation falls outside safe
    parameters will immediately raise an alert, and will be checked by our SRE team. Many of those components will
    automatically be recycled or restarted by our monitoring systems.

    In the case of *any* on-going issue affecting Divio infrastructure, we will post a notice on
    https://status.divio.com.


Action without information is useless
-------------------------------------

It is almost impossible to address any performance problem without adequately understanding its causes. Any action
attempting to resolve the problem without a good understanding of its nature is simply a shot in the dark with little
chance of success.

It is tempting to consider upgrading a subscription (i.e. increasing resources such as RAM and CPU) as an immediate
first resort, but - as much as Divio will be pleased to see you spending more money on our services - this should be
resisted.


Use Application Performance Monitoring
---------------------------------------

The single most useful thing at your disposal when trying to identify the cause of a performance issue is an
**Application Performance Monitoring** tool. There is nothing that provides an equally valuable insight into what an
application is actually doing - how long it spends dealing with a particular request, or kind of request, and the code
pathways a request invokes.

It can quickly become apparent whether a slow response is being held up in straightforward computational processing,
database or file interaction, template rendering or other process. (For example, if it turns out that a certain request
triggers a very expensive database query, then there is no amount of other resources that can be thrown at the
application to improve performance: the only solution is to optimise the query, or ensure that its results can be
cached as much as possible. If the query takes so long to process that the request times out before the database can
return a result, then only rewriting the query will be solution.)

Well-established APM solutions suitable for web applications include New Relic and Elastic APM. Most well-known
services offer integration packages for multiple different languages.

For any mission-critical application or serious effort to identify performance shortfalls, we strongly recommend
using APM. A little investment in APM can save you great expenditure in time, effort and money.


Use other tools
----------------

All other tools are second-best to APM, and none of them can take its place. However, there are numerous other options
that help provide some level of insight all the same.

Metrics
~~~~~~~~~~~

All Divio projects include :ref:`metrics <metrics>`. As well as showing whether an application is consuming excessive
resources, metrics can also show when changes in consumption occurred (for example, following deployment of new code).

In most cases, users will find that their under-performing application is not in fact running out of RAM or CPU - a
clear indication that adding resources by upgrading a subscription will not be a solution.

You may find that RAM and/or CPU consumption are reaching exceeding expected values. These can both in themselves cause
degraded performance. In that case, it is *possible* that the application should be allocated more resources, but it is
equally likely that finding ways to reduce its resource consumption will be a better solution (a memory leak for
example will not be solved by adding more RAM).


Runtime logs
~~~~~~~~~~~~~~~~~~~~

All Divio projects provide runtime logs, accessible from the Environments view as well as from the terminal (e.g.
``divio app logs --tail live``). Logs show for example how long requests take to serve and reporting internal
errors, but this provides only a basic insight into behaviour. However, as with metrics, referring to runtime logs can
help eliminate suspects from your enquiries quite quickly.


Debug tools
^^^^^^^^^^^

Debug tools (such as Django Debug Toolbar), though not fully-fledged APM products, can also provide a degree of insight
into an application's performance, especially when investigating the behaviour of an application when dealing with a
particular request, and can be easier to set up and use. They are especially useful in development environments.

