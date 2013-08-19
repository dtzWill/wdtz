Bootstraped
==============

A Jinja2 based theme for [Pelican](http://blog.getpelican.com/).  
It heavily depends on the [Bootstrap Framework](http://twitter.github.com/bootstrap/).  

Extra Variables
===============
The following are extra variables that you can include in your 
site's config.

## DEFAULT_TRUNCATE ##
Allows you to customize the size of the except shown at the main
page for categories and the index page.

This expects a integer. The number is the number of characters.

Example: DEFAULT_TRUNCATE = 500

## NON_GENERIC_BOOTSTRAP ##
Allows you to use a non-default theme for bootstrap. Since the 
theme for bootstrap is boring I also include the following themes
from [bootswatch](http://bootswatch.com/):
*      [Cosmo](http://bootswatch.com/cosmo)
*      [Cyborg](http://bootswatch.com/cyborg)
*      [Simplex](http://bootswatch.com/simplex)
*      [Slate](http://bootswatch.com/slate)
*      [Spacelab](http://bootswatch.com/spacelab)

Example: NON_GENERIC_BOOTSTRAP = "simplex"