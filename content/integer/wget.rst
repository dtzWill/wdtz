Analysis of Integer Error in Latest wget
########################################

:tags: integer, signedness, bug, wget
:date: 2013-08-19 14:03

Here's another integer error found by our research
that occurs in wget 1.14 (latest at time of writing)
in the ``--version`` output.

This has been reported and fixed upstream,
coming soon to a wget near you!

PELICAN_END_SUMMARY

Description
-----------

The error is a signedness comparison issue
in ``format_and_print_line()`` used by wget's
``--version`` to print information such as
the flags used to the compiler and linker
when wget was built.

Relevant code from src/main.c:

.. code-block:: c

  int remaining_chars;
  ...
  token = strtok (line_dup, " ");
  while (token != NULL)
    {
      /* If however a token is much larger than the maximum
         line length, all bets are off and we simply print the
         token on the next line. */
      if (remaining_chars <= strlen (token))
        {
          if (printf ("\n%*c", TABULATION, ' ') < 0)
            return -1;
          remaining_chars = line_length - TABULATION;
        }
      if (printf ("%s ", token) < 0)
        return -1;
      remaining_chars -= strlen (token) + 1;  /* account for " " */
      token = strtok (NULL, " ");
    }

Where if ``remaining_chars`` goes negative the comparison
``remaining_chars <= strlen (token)`` erroneously returns
true, causing all remaining tokens to be printed on the same
line instead of being wrapped.

When the printed string contains a token longer than
the wrapping width (``line_length - TABULATION`` in the above)
``remaining_chars`` will go negative and trigger this issue.  Humorously we encountered this issue only because of a very long flag used by our research compiler that took a path name as an argument.

Status
------

This issue has been reported_, and is now fixed upstream_
thanks to the wget developers working with me on the issue.
While touching that code, also prettified wget's
``--version`` output in general (see below), and scored
my first (minor) entry on a GNU tool's ChangeLog.  Woo!

Example
-------

Before:

::

  GNU Wget 1.14.74-8bf9-dirty built on linux-gnu.
   
  +digest +https +ipv6 +iri +large-file +nls +ntlm +opie +ssl/gnutls 
  
  Wgetrc: 
      /usr/local/etc/wgetrc (system)
  Locale: /usr/local/share/locale 
  Compile: gcc -DHAVE_CONFIG_H -DSYSTEM_WGETRC="/usr/local/etc/wgetrc" 
      -DLOCALEDIR="/usr/local/share/locale" -I. -I../lib -I../lib 
      -DUNIMPORTANT_TEXT_TO_CREATE_VERY_LONG_TOKEN_IN_FLAG_STRING=123456789 -O2 -g 
  Link: gcc 
      -DUNIMPORTANT_TEXT_TO_CREATE_VERY_LONG_TOKEN_IN_FLAG_STRING=123456789 -O2 -g -lnettle -lgnutls -lgcrypt -lgpg-error -lz -lz -lidn -luuid -lpcre ftp-opie.o gnutls.o http-ntlm.o ../lib/libgnu.a

After:

::

  GNU Wget 1.14.74-8bf9-dirty built on linux-gnu.
   
  +digest +https +ipv6 +iri +large-file +nls +ntlm +opie +ssl/gnutls 
  
  Wgetrc: 
      /usr/local/etc/wgetrc (system)
  Locale: 
      /usr/local/share/locale 
  Compile: 
      gcc -DHAVE_CONFIG_H -DSYSTEM_WGETRC="/usr/local/etc/wgetrc" 
      -DLOCALEDIR="/usr/local/share/locale" -I. -I../lib -I../lib 
      -DUNIMPORTANT_TEXT_TO_CREATE_VERY_LONG_TOKEN_IN_FLAG_STRING=123456789 
      -O2 -g 
  Link: 
      gcc 
      -DUNIMPORTANT_TEXT_TO_CREATE_VERY_LONG_TOKEN_IN_FLAG_STRING=123456789 
      -O2 -g -lnettle -lgnutls -lgcrypt -lgpg-error -lz -lz -lidn -luuid 
      -lpcre ftp-opie.o gnutls.o http-ntlm.o ../lib/libgnu.a 

---------------

References:
-----------

.. target-notes::

.. _reported: https://savannah.gnu.org/bugs/index.php?39453
.. _upstream: http://git.savannah.gnu.org/cgit/wget.git/commit/?id=a12bd59111bd5e6fba91a8f1fa6c09698d03f740
