Freenode SASL Upgrade: Irssi HOWTO
##################################

:date: 2015-01-05 12:25
:tags: irssi, sasl, freenode, irc, network, guide

The freenode_ IRC network has for a long time supported
connecting and automatic identification using SASL_.

Recently, the freenode network deprecated the commonly used
SASL mechanism ``DH-BLOWFISH`` due to security concerns,
causing my IRC client (irssi_) to no longer be able to
authenticate.

Unfortunately, while scripts and guides describing using
irssi with ``DH-BLOWFISH`` are plentiful, it seems the steps
required to use the new preferred
``ECDSA-NIST256P-CHALLENGE`` method are not yet documented.

Read on for a step-by-step walk-through of configuring
irssi to use SASL with freenode in 2015.

PELICAN_END_SUMMARY

Background
==========

Recently `freenode upgraded to Atheme 7.2`_, and in the
process deprecated support for the SASL mechanism
``DH-BLOWFISH``.
Atheme is the reference implementation of the current IRC
protocol, which `deprecates DH-BLOWFISH in IRCv3`_.

There are good reasons for this change, but regardless it's
been done and irssi needs some help accommodating this
change.

Why not PLAIN?
--------------

It would be remiss not to mention that the simplest solution
to this problem is to use the ``PLAIN`` SASL method in
conjunction with SSL.  Clients configured in this way will
work with the new services just like they have previously,
with similar security properties.

While it is not my goal to convince you ``PLAIN`` is
insufficient, there is benefit in using a SASL method other
than ``PLAIN`` in a defense-in-depth sort of way.  Should
the SSL stream become compromised in some manner, ``PLAIN``
would make obtaining a user's password as easy as forcing a
reconnect, while the other mechanisms provide additional
layers of security.

Use SSL!
--------
Regardless of the SASL method being used, if you're
bothering with any of this the first and most effective step
to securing your IRC connection is using SSL.
SSL is supported by virtually all IRC networks and requires
only trivial configuration in most clients.

Be sure your client validates the server's certificate
properly (strict SSL) or your connection is trivially
vulnerable to MITM_ attacks.

Why SASL in addition to SSL
---------------------------

Common implementations give SASL users one benefit not
generally available to other users: with SASL, network
services recognize you before you even are active on the
network, which can be useful when making use of services
like a hostname cloak or automatically joining channels only
open to invited accounts.

As an aside, as far as I can tell client-side certificates
(like those used with CertFP_ identification) could be used
to provide similar benefits but this doesn't seem to be done
on any network I'm familiar with.
One possible explanation is that since CertFP doesn't work
with Tor (I believe?), implementation efforts focus on SASL
which is available to all users.

Other reasons include additional layers of security in terms
of protecting the account password, and policies such as
`freenode's requirement of SASL when connecting over Tor`_.

Configuring Irssi to use ECDSA-NIST256p-CHALLENGE
=================================================

1) Install ecdsatool
--------------------

First, download and build a copy of ecdsatool_.
This wasn't available as a package for my server's
distribution, so I built is as follows:

.. code-block:: console

  $ git clone https://github.com/atheme/ecdsatool.git
  $ cd ecdsatool
  $ ./autogen.sh
  $ ./configure --prefix=$HOME/local
  $ make -j
  $ make install

Standard build recipe, tweak as you see fit.

Afterwards, be sure the resulting ``ecdsatool`` utility is
available on your shell's ``PATH`` so the irssi script we
configure later will be able to find and use it.

2) Generate key pair
--------------------

Next, use ``ecdsatool`` to generate a key pair for SASL use:

.. code-block:: console

  $ mkdir -p ~/.irssi/certs
  $ ecdsatool keygen ~/.irssi/certs/freenode.pem

I keep my IRC-related certificates in ``~/.irssi/certs``,
personal preference.

3) Install cap_sasl script
--------------------------

Next, grab a copy of the ``cap_sasl.pl`` script shipped
in the ecdsatool repository:

.. code-block:: console

  $ mkdir -p ~/.irssi/scripts
  $ wget https://raw.githubusercontent.com/atheme/ecdsatool/master/cap_sasl.pl -O ~/.irssi/scripts/cap_sasl.pl

Additionally you likely want to have the script loaded when
irssi starts:

.. code-block:: console

  $ mkdir -p ~/.irssi/scripts/autorun
  $ ln -s ../cap_sasl.pl ~/.irssi/scripts/autorun/

4) Configure SASL for freenode
------------------------------

From within irssi, use the ``/sasl set`` command to indicate
what username and certificate to use for your IRC network:

.. code-block:: console

  $ irssi
  ...

.. code-block:: plain

  /sasl set freenode username /full/path/to/freenode.pem ECDSA-NIST256P-CHALLENGE

Replacing ``freenode`` with the network name your configured
in irssi, ``username`` with your freenode account name, and
the path with a full path to the key pair generated earlier.

Afterwards, be sure to save this information for future use:

.. code-block:: plain

  /sasl save

The result should be an entry in ``~/.irssi/sasl.auth`` that looks something like this:

.. code-block:: plain

  freenode dtzWill /home/will/.irssi/certs/freenode.pem ECDSA-NIST256P-CHALLENGE


5) Register Public Key with NickServ
------------------------------------

Almost there! Final step is to give NickServ the public key
portion of our key pair so it can recognize your client and
associate it with your account.

First, grab the ``pubkey`` from the key pair:

.. code-block:: console

  $ ecdsatool pubkey ~/.irssi/certs/freenode.pem

Next, connect to freenode and identify yourself as you would usually.

Finally, tell NickServ about your public key:

.. code-block:: plain

  /msg nickserv set property pubkey ArRZ4XCwSFYhT7RH5Ms7dosJEm8OYLO3gWSSGQCsYOCk


Replacing the example public key with what was printed by ``ecdsatool`` in the previous step.

6) Done! Reconnect and Test
---------------------------

At this point you have all the pieces required to use SASL
with the ``ECDSA-NIST256P-CHALLENGE`` mechanism to connect
to freenode.
Disconnect from freenode and reconnect to try it out!

If successful, you should see something like this:

.. code-block:: plain

  14:50 -!- Irssi: CLICAP: supported by server: account-notify extended-join identify-msg multi-prefix sasl
  14:50 -!- Irssi: CLICAP: requesting: multi-prefix sasl
  14:50 -!- Irssi: CLICAP: now enabled: multi-prefix sasl
  14:50 -!- will!will@unaffiliated/dtzwill dtzWill You are now logged in as dtzWill.
  14:50 -!- Irssi: SASL authentication successful

Alternative Method Without ecdsatool
====================================

It appears that there is another solution that does not
require the use of an external tool like ``ecdsatool`` by
using the ``Crypt::PK::ECC`` perl module.

This script is available in the Atheme git repository:
`cap_sasl.pl git`_.
In addition to no longer requiring an external tool, the
script offers a ``keygen`` command that should make setup
easier.

I haven't tried this script yet myself, as I didn't discover
it until well after I completed the procedure described
above.
Additionally, the module is uses doesn't seem to be
available as a package on any of my systems although it can
of course be obtained using cpan_.

If you try this method and have success, please report back.

(Update: March 03, 2015)
------------------------

Jesper Freesbug from the comments was kind enough to share
his experiences and provide a walkthrough of the setup
process when using this approach.  I've featured this
comment below and recommend taking a look if you're
interested in this solution.

In addition to the FreeBSD package he mentions, it seems
other systems also provide the required perl module as part
of a ``cryptx`` package.  For example, on Arch it's
available as an AUR package named ``perl-cryptx``.
Hopefully the module is made more universally available in
the future.

Closing Thoughts
================

It seems the folks working on Atheme and freenode are hard
at work improving the services that are widely used in a
variety of communities.
While this post is motivated by a lack of documentation, the
procedure is simple and it has been mentioned in multiple
places time that they hope to both document this thoroughly
soon and to improve the workflow for users.
Huge thanks to those folks, and for offering all of this
work for free for users like myself to enjoy.

Additionally, all of this is arguably something an IRC
client should support natively or at least help facilitate.
This is how some folks feel and have opened an issue
on the `irssi github`_.

Hope this helps, and let me know if you have any questions or issues.  Enjoy!


References
==========
.. target-notes::

.. _freenode: http://freenode.net/
.. _SASL: http://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer
.. _irssi: http://irssi.org/
.. _freenode upgraded to Atheme 7.2: http://blog.freenode.net/2014/11/atheme-7-2-and-freenode/
.. _deprecates DH-BLOWFISH in IRCv3: http://ircv3.atheme.org/documentation/sasl-dh-blowfish
.. _MITM: http://en.wikipedia.org/wiki/Man-in-the-middle_attack
.. _CertFP: https://freenode.net/certfp/
.. _freenode's requirement of SASL when connecting over Tor: https://freenode.net/irc_servers.shtml#tor
.. _ecdsatool: https://github.com/atheme/ecdsatool
.. _cap_sasl.pl git: https://raw.githubusercontent.com/atheme/atheme/master/contrib/cap_sasl.pl
.. _cpan: http://www.cpan.org/
.. _irssi github: https://github.com/irssi/irssi/issues/4

