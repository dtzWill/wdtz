New Website
###########

:date: 2013-08-19 9:00
:tags: first post, pelican


Obligatory post announcing new website:
changes, lessons, and a chance
to give the new site a spin.

Maybe I'll stick with the whole blog
thing this time around :).

PELICAN_END_SUMMARY

Why Pelican
-----------

I finally replaced the old Wordpress_-based website with one
based on Pelican_.  Pelican is a static site generator which
is appealing to me for the following reasons:

* Content creation can be done from the comfort of vim
* CLI goodness for deployment
* git goodness for easy backup, content management, and writing on-the-go
* super-easy to host, allowing me to drop php and mysql support on my server.

... which is basically what is listed on the Pelican website.  Good work.

First few reasons just make me happy, which is especially
important if I'm going to succeed at actually posting
periodically.

The last reason is technical, but important because the server running
this site is on its last legs (and was reject hardware years ago).
As an added bonus I no longer have to worry about a wordpress
vulnerability giving my site to some hacker.  Being able to
trivially deploy to an alternate host should my server go
down is also a nice comfort.

Finally, Pelican is used for kernel.org_.  Good enough for them,
good enough for me.

External
--------

For the curious, here's the components used to build this website:

Git repository: github_

Pelican theme used: bootstraped_

Bootstrap coloring: Cyborg_

Lessons
-------

* Never underestimate how much time can be lost redesigning a website.
* Nothing makes you go "didn't need those files anyway" like a runaway script
* Pelican_ is awesome
* I believe I now understand the appeal of formats like
  rst_:
  More writing, less formatting.
* Writing (even this post!) is remarkably hard.  Practice
  makes perfect.

---------------

References
----------

.. target-notes::

.. _Wordpress: http://wordpress.com
.. _Pelican: http://getpelican.com
.. _kernel.org: http://kernel.org
.. _github: https://github.com/dtzWill/wdtz
.. _bootstraped: https://github.com/masterkoppa/Pelican-Themes/tree/master/bootstraped
.. _Cyborg: http://bootswatch.com/cyborg/
.. _rst: http://docutils.sourceforge.net/rst.html
