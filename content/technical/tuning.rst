Easy Website Tuning
###################

:date: 2013-08-25 20:12
:tags: pelican, server tuning, webdev

Having recently moved to Pelican_,
I found myself interested in seeing
how I could coerce my server (runing Apache_)
into taking proper advantage of the bulk
of the website being static.

There's lots of information on the subject
out there, but below I describe the few
easy changes I made to greatly improve
performance of my website.

PELICAN_END_SUMMARY

Tunables
========

Enable gzip compression
-----------------------

Ensure you have ``mod_deflate`` available and add
the following to your httpd.conf:

.. code-block:: apache

  <IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/text text/html text/plain text/xml text/css application/x-javascript application/javascript application/json
  </IfModule>

Which enables gzip compression on the listed file
types, which is simple and appropriate for a
Pelican_-based website.

While trimming some of my larger dependencies
(such as the bootstrap js and css) would be
useful, gzip compression is simple and very
effective on text-based formats such as these.

Since compression support is used automatically in
response to the client's reported support for it,
I was happy to note that ``mod_deflate``
automaticaly adds an appropriate ``Vary:
Accept-Encoding`` header to enable correct
functionality even when accessed through a proxy.

Set the "Cache-Control" header
------------------------------

This header is used to specify the
caching behavior of the client,
and when used properly can greatly
reduce accesses made to unchanging
files while browsing your site.

To add these headers, one can make
use of ``mod_expires`` or by simply
adding something like the following:

.. code-block:: apache

  <FilesMatch "\.(ico|pdf|flv|jpg|jpeg|png|gif|js|css|swf)$">
    Header set Cache-Control "max-age=29030400, public"
  </FilesMatch>

This example says the content is
*public*, which allows any intermediate host
to cache the contents.  For static resources
like those matched by this directive,
this is reasonable behavior.  You would
not want this to be set for content
generated for a particular user.

The ``max-age`` component specifies how
long (in seconds) the content can be cached.

Use a CDN
=========

From Wikipedia, a CDN_ is:

  A content delivery network or content distribution network
  (CDN) is a large distributed system of servers deployed in
  multiple data centers across the Internet. The goal of a CDN
  is to serve content to end-users with high availability and
  high performance.

In short, CDN's are used to provide high-speed
access to a file by providing the data from a
server "close" to the user accessing it.

Outsourcing Dependency Hosting
------------------------------

While the content of my blog is small (text mostly), it does have
some moderately hefty dependencies:

* Bootstrap_: Provides primary design elements used by this site
* jquery_: Bootstrap dependency
* `Font Awesome`_: Scalable icons without need for images
* Bootswatch_: For theming bootstrap

Luckily there are a number of free CDN's that host very
common files such as these.  These are maintained by large
companies with the explicit purpose of being highly
available and very fast, enabling users accessing my site to
get copies of these dependencies much faster than I'd be
able to provide them otherwise.

The CDN's I'm now using are:

* `Bootstrap CDN`_: Used to host my Bootstrap, Font-Awesome, and theme dependencies.
* `Google Hosted Libraries`_: Hosts jquery

CDN Example
-----------

An example of rewriting some self-hosted dependencies to use
CDN-hosted sources is shown below:

Before:

.. code-block:: html

  <link rel="stylesheet" href="{{ SITEURL }}/theme/css/bootstrap.min.css" type="text/css" />

After:

.. code-block:: html

  <link href="//netdna.bootstrapcdn.com/bootstrap/2.3.2/css/bootstrap.min.css" rel="stylesheet">

Where ``{{ SITEURL }}`` is part of the templating done by
Pelican_, and the ``//`` prefix to the CDN source is a trick
to use http or https dependencing on how the current page is
loaded.

Tools to Spot Easy Tunables
===========================

While investigating how to improve my website's loading times,
I ran into three tools that were particularly useful.

GTMetrix
--------

`GTMetrix`_

Providing a page load waterfall graph, YSlow/PageSpeed scores with detailed explanations,
this was my favorite as the most comprehensive of these tools.

Pingdom
-------

`Pingdom Website Speed Test`_

Also offers a waterfall, and another "Page Speed" analysis that found
other problems not reported by GTMetrix.

Google
------

`Google PageSpeed Insights`_

Google's offering based on its PageSpeed_ service, this was particularly helpful
in identifying issues for mobile users.  They also offer plugins that run
on your server and automatically optimize your website.  While very cool
and appealing, I didn't explore this route since I was interested
in the learning to be had by exploring this by hand.

Summary
=======

This blog now loads quite a bit faster, and ignoring time happily spent
reading up on the various topics discussed here the actual
changes were straightforward and easy.  Hope this helps!

---------------

References
==========

.. target-notes::

.. _Pelican: http://getpelican.com
.. _Apache: http://httpd.apache.org/
.. _CDN: http://en.wikipedia.org/wiki/Content_delivery_network
.. _Bootstrap: http://getbootstrap.com/
.. _jquery: http://jquery.com/
.. _Font Awesome: http://fortawesome.github.io/Font-Awesome/
.. _Bootswatch: http://bootswatch.com/
.. _Bootstrap CDN: http://www.bootstrapcdn.com/
.. _Google Hosted Libraries: https://developers.google.com/speed/libraries/devguide?hl=ja#Libraries
.. _Pingdom Website Speed Test: http://tools.pingdom.com/fpt/
.. _GTMetrix: http://gtmetrix.com/
.. _Google PageSpeed Insights: https://developers.google.com/speed/pagespeed/insights/
.. _PageSpeed: https://developers.google.com/speed/pagespeed/
