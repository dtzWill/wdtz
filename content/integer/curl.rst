Curl Globbing Bugs
##################

:date: 2013-08-19

I recently discovered a slew of bugs in curl_,
which occur in all versions I have access to,
including latest release at time of writing (7.32.0)
and goes back to at least 7.19.7.

One of the bugs can be used to crash curl
or systems using curl via exec (not libcurl),
the others cause strange or incorrect behavior.

PELICAN_END_SUMMARY

The bugs in question are:

* crasher_ due to bad error handling
* sscanf_-based parsing overflow
* `input validation`_ bug on the ''step'' portion of a range glob
* `URL count overflow`_ bug triggered by globbing for a ridiculous number of URL's

These have all been fixed now, first as part of a general
`globbing overhaul`_ commit, followed by a specific
`URL overflow checking`_ fix.

See the bug reports for details on the errors and example
invocations, hopefully a release fixing these issues is made
soon.

These errors were encountered during my research on integer
overflows, and I'm glad the developer fixed them so quickly!
Hopefully these fixes will reach everyone in the form of a
new release soon :).

References
==========

.. target-notes::

.. _curl: http://curl.haxx.se/
.. _crasher: https://sourceforge.net/p/curl/bugs/1264
.. _sscanf: https://sourceforge.net/p/curl/bugs/1265
.. _input validation: https://sourceforge.net/p/curl/bugs/1266
.. _URL count overflow: https://sourceforge.net/p/curl/bugs/1267
.. _globbing overhaul: https://github.com/bagder/curl/commit/5ca96cb84410270e233c92bf1b2583cba40c3fad
.. _URL overflow checking: https://github.com/bagder/curl/commit/f15a88f2b25ee44d8c8d3bdcf2508fdf50f8b868
