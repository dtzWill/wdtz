IOC Journal Edition: Highlights
###############################

:date: 2015-12-07 11:41
:tags: integer, academia, undefined, bug
:status: draft

I'm excited to announce the publication of the
`journal version of "Understanding Integer Overflow in C/C++"`_, appearing
in `TOSEM Volume 25 Issue 1`_.
This is an updated and expanded version of our `ICSE12 paper`_ of the same name.

The longer journal format enabled a more thorough treatment of the subject, and
we did our best to take advantage of that opportunity.

Highlights of what's new:

PELICAN_END_SUMMARY

* Automated large-scale study of overflows in top 10,000 Debian packages (§6)
* More thorough discussion and explanation of integer behavior, including implementation-defined behavior and usual arithmetic conversions (§§ 2, 3.1, 3.2)
* Implementing recoverable checks efficiently: experience and two new optimizations (§4.4)
* Deployment experiences and resulting improvements useful for anyone making compiler-based tools for the real world (§5).

The Debian experiment was particularly fun and had many interesting results.
Full results are available on request, and we provide a `complete version of selected results presented in Table VI`_ online.

Let me know if you'd like to discuss our findings or the paper.  Enjoy!

---------------

References
----------
.. target-notes::


.. _journal version of "Understanding Integer Overflow in C/C++": http://dx.doi.org/10.1145/2743019
.. _TOSEM Volume 25 Issue 1: http://tosem.acm.org/archive.cfm?id=2852270
.. _ICSE12 paper: http://www.cs.utah.edu/~regehr/papers/overflow12.pdf
.. _complete version of selected results presented in Table VI: http://wdtz.org/files/ioc-debian.log
