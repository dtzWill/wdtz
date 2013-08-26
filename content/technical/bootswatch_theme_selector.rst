Bootswatch Theme Selector
#########################

:date: 2013-08-25 21:54
:tags: webdev

Despite my passion for light-on-dark themes,
not everyone finds them as readable and enjoyable
as I do.  To address these concerns I investigated
what it would take to add a drop-down to this website
to enable dynamic selection of themes by the user.

.. figure:: /images/bootswatch_theme_dropdown.png
   :alt: bootswatch theme dropdown
   :align: center
   :figclass: text-center

   Bootswatch Theme Dropdown

The relevant code is given, but for those
interested in a complete example take a look
at the `website github`_.

PELICAN_END_SUMMARY

Adding the Dropdown
===================

The drop-down is based on a `StackOverflow post`_,
modified to select a Bootswatch theme dynamically.

First, the HTML component of the drop-down:

.. code-block:: html

  <li class="dropdown" id="theme-dropdown">
    <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="icon-cogs icon-large"></i> Theme<b class="caret"></b></a>
    <ul class="dropdown-menu">
      <li><a href="#" class="change-style-menu-item" rel="cyborg"><i class="icon-fixed-width icon-pencil"></i> Cyborg (Default)</a></li>
      <li><a href="#" class="change-style-menu-item" rel="cerulean"><i class="icon-fixed-width icon-pencil"></i> Cerulean</a></li>
      <li><a href="#" class="change-style-menu-item" rel="cosmo"><i class="icon-fixed-width icon-pencil"></i> Cosmo</a></li>
      <li><a href="#" class="change-style-menu-item" rel="flatly"><i class="icon-fixed-width icon-pencil"></i> Flatly</a></li>
      <li><a href="#" class="change-style-menu-item" rel="journal"><i class="icon-fixed-width icon-pencil"></i> Journal</a></li>
      <li><a href="#" class="change-style-menu-item" rel="readable"><i class="icon-fixed-width icon-pencil"></i> Readable</a></li>
      <li><a href="#" class="change-style-menu-item" rel="slate"><i class="icon-fixed-width icon-pencil"></i> Slate</a></li>
      <li><a href="#" class="change-style-menu-item" rel="spacelab"><i class="icon-fixed-width icon-pencil"></i> Spacelab</a></li>
    </ul>
  </li>

Which as-written belongs in the navbar of your
Bootstrap-based site.  Here I have drop-down items for my
preferred Bootswatch themes, but the format should
straightforward to add/remove as you see fit.

The important tidbits are the
``class="change-style-menu-item"`` and ``rel="spacelab"``
fields of the theme links, the rest is Bootstrap-specific
code for putting it all into a drop-down.

Additionally, we're going to modify the primary bootswatch
theme link by adding a title to it for easy lookup from
javascript later:

.. code-block:: html

  <link href="//netdna.bootstrapcdn.com/bootswatch/3.0.0/cyborg/bootstrap.min.css" rel="stylesheet" title="main">

Javascript
----------

Now to perform the desired theme change,
add the following jquery function:

.. code-block:: js

    /* When a theme-change item is selected, update theme */
    jQuery(function($) {
        $('body').on('click', '.change-style-menu-item', function() {
          var theme_name = $(this).attr('rel');
          var theme = "//netdna.bootstrapcdn.com/bootswatch/3.0.0/" + theme_name + "/bootstrap.min.css";
          set_theme(theme);
        });
    });


What does this do?  This adds a function to each of the
``change-style-menu-item`` links we added in our HTML
earlier which is triggered when the link is clicked.

When invoked, this function extracts the value of the ``rel`` attribute
of the clicked link, and uses it to invoke ``set_theme``
with an appropriate replacement CSS URL.

Below is a tentative definition for ``set_theme`` that we'll
be replacing in the following section.

.. code-block:: js

    function set_theme(theme) {
      $('link[title="main"]').attr('href', theme);
    }

Making The Selection Persist
============================

What we've done so far adds the drop-down and lets users
change the theme.  That's nifty and highlights the magic
of Bootswatch themes, but what if we wanted to make
the user's selection persist across visits and
as they navigate the site?

To accomplish this I opted to use HTML5's
`local storage`_ feature.  Being a simple blog
without a concept of users, stashing this server-side
makes little sense, and local storage is supported
by all modern browsers and is very easy to use.

Saving Theme with Local Storage
-------------------------------

First, we add a function to determine if the user supports
the local storage feature.  This helps avoid errors on
browsers without support or with the feature disabled:

.. code-block:: js

    function supports_html5_storage() {
      try {
        return 'localStorage' in window && window['localStorage'] !== null;
      } catch (e) {
        return false;
      }
    }

    var supports_storage = supports_html5_storage();


Next let's replace our ``set_theme()`` function with one that
saves the selected them into local storage:

.. code-block:: js

    function set_theme(theme) {
      $('link[title="main"]').attr('href', theme);
      if (supports_storage) {
        localStorage.theme = theme;
      }
    }

Finally, add code to load the setting and apply it
if we find the user has a saved theme choice:

.. code-block:: js

    /* On load, set theme from local storage */
    if (supports_storage) {
      var theme = localStorage.theme;
      if (theme) {
        set_theme(theme);
      }
    } else {
      /* Don't annoy user with options that don't persist */
      $('#theme-dropdown').hide();
    }

Where I chose to hide the drop-down altogether for
clients that don't support local storage.

Selectively Enabling on Development Builds
==========================================

Ultimately I decided to not publish this on the
production version of the website, only enabling
it in development builds.  A website's design
is an important part of capturing the author's
voice and by giving control over this to visitors
the expressivity of the blog is weakened.  Kudos
to my friend Brian for pointing this out.

In this section I describe the easy Pelican-specific changes
needed to only include the theme-selection code in
development but not in production builds.

First, I added the following new definition to ``pelicanconf.py``:

.. code-block:: python3

  THEME_CHANGER = True

and the following to ``publishconf.py``:

.. code-block:: python3

  THEME_CHANGER = False

Next, I wrapped the various HTML and javascript
components in ``base.html`` with

.. code-block:: jinja

  {% if THEME_CHANGER %}
    ...
  {% endif %}


Which has an effect very much like C preprocessor ``#ifdef
THEME_CHANGER`` ... ``#endif``, only including the theme
switcher dropdown and supporting javascript when not using
the publish configuration.

---------------

References
==========

.. target-notes::

.. _website github: https://github.com/dtzWill/wdtz
.. _StackOverflow post: http://stackoverflow.com/a/17541994
.. _local storage: http://diveintohtml5.info/storage.html
