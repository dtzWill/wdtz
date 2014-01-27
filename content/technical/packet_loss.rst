Mysterious Lag Spikes and Faulty Switches
#########################################

:date: 2014-01-23 12:06
:tags: network

My residential internet experience has always been poor, so
when I started observing bizarre network behavior a few
months back I attributed it to upstream problems and wrote
it off with a sigh.  The issue persisted however,
so over the winter break I decided to sit down
and tackle it once and for all.

Tracking down the source of the issue was an interesting
adventure, and ultimately the problem was in the last
place I thought to check: a pair of TEG-S80g unmanaged
gigabit switches made by TRENDnet.

**Do not buy!** :)

Details follow.

PELICAN_END_SUMMARY

The Problem
-----------

First, let's start with the symptom: a particular
online game was experiencing very severe "lag spikes"
every 60 seconds or so where it would seem I was
temporarily disconnected from the server.
This would last a few seconds then go back to normal.

Usually this sort of issue has simple explanations:
local modem temporarily lost connection with ISP,
a backup job is saturating my link causing packet
loss, or there's transient upstream issue with
either my ISP or the game server.

Unfortunately all the likely candidates were quickly ruled
out.  Connectivity was never lost as I was able to video chat
over Skype continuously through these events and
the logs on my modem were clean.  This made me all
the more curious.

An upstream issue was a potential cause, but if so it was
a rather bizarre one: others on same server did not
experience similar issues, and further investigation
showed during these periods my game client was not
sending packets to my router at all which is strange.

Here's a graph of network activity measured by
my router during these periods:

.. figure:: /images/packet_loss/problem_graph.png
   :alt: network activity graph during lag spikes
   :align: center

   Network Activity Graph -
   The various dips to zero correspond with issues in-game.

The graph above shows network activity sampled every 3 seconds
over a period of 4 minutes, and the drops to zero correspond
with in-game issues.  This selection of traffic shows at
least 6 outages of around 3 seconds during the 4-minute
period.

This issue persisted for months since it only
had an impact on my weekly game nights with
my brother and we were still mostly able
to play.  However, over the recent holiday
break I finally caved and treated myself
to a day of diving into this issue
in an attempt to finally answer the question
that had been bugging me for months:

**What's going on?**

A Step Forward
--------------

The first big breakthrough was the ability
to reproduce this problem without
using my console or the game in question.
This enabled easily testing from various
parts of my network and more importantly
ruled out a buggy game client or server.

While gathering all the information I could
about the network normally and during
these periods I discovered the fantastic
`NetAlyzr`_ tool from Berkeley.
This tool is an automated Java program that tests
for a number of common network problems and
reports them back to you.

The two most interesting issues turned up
from the `initial NetAlyzr results`_ indicated
I was suffering from the famous `buffer bloat`_
problem, and experiencing
**bursts of packet loss**.
There's not much I can do to change the size of
buffers upstream, but packet loss sure sounds
related!

But what exactly does it mean by packet loss?
How is this measured? Is this something to contact
my ISP about?  Unfortunately I was unable
to find answers to these questions in the
documentation, and couldn't figure it out
from the code since the tool isn't open-source.

To the debug-mobile!

"Bursts of Packet Loss"?
------------------------

To understand what the NetAlyzr tool was doing,
I captured the network traffic it sent and
received using `Wireshark`_.  Together with
the server/client logs linked from the NetAlyzr
results page, I determined the tool exchanges
UDP packets every 20ms while running other
tests.  This traffic communicates with their
server on the same port as other tests
executed concurrently so it takes a little
analysis for each capture to identify
the port used by the local endpoint.

Having filtered out the packet-loss-testing
traffic I graphed the packets/second to
look for issues:

.. figure:: /images/packet_loss/old_switch.png
   :alt: packet loss during NetAlyzr run
   :align: center

   Captured NetAlyzr activity - black shows
   traffic by the packet loss test, red shows
   overall traffic.  Packet loss occurs
   around 84s to 87s and is marked
   with a blue circle.

There's the packet loss (see the blue circle)!
But why is this happening?
Note the loss didn't happen during an earlier
traffic burst that peaked to about 10x higher,
suggesting something more subtle than
"packets are dropped under high load".

To debug this, I started testing from various
points in the network starting with connecting
straight to my modem, then directly
to the router, working back towards my desktop.

I was surprised to discover the only location
between my desktop and modem that suffered
packet loss was when testing through my switch!

I immediately replaced the cable from
the switch to my router, which had no
effect.  Similarly testing using that cable
directly resolved the packet loss issue.
Additionally this occurred regardless
which of the ports on the switch were used.

Starting to suspect my switch was somehow
to blame, I tried the procedure from an identical
switch in the living room.  Same results:
packet loss when testing through the switch,
none when testing using the cable leading
to it.

...What?

Unfortunately my attempts to reproduce
this packet loss using my own synthetic
tests all failed, using various streams of
TCP and UDP data with the nifty `iperf`_ tool.
I only saw packet loss under traffic loads
that saturated the link, which is of course
the expected behavior.

I confirmed the game performed
properly when I removed the switch
from the network topology, which
was both relieving and frustrating:
what kind of junk switch drops
packet streams under these
basic circumstances?

Replacement
-----------
I ended up purchasing replacement
`switches from TP-LINK`_ that
have completely resolved the issue.

My `new NetAlyzr results`_ no longer
indicate packet loss, and the game
finally works as it should.  Now,
if only I was any good at it :D.

Graphing a capture of the new results
no longer shows the interrupted
connection:

.. figure:: /images/packet_loss/new_switch.png
   :alt: No packet loss during NetAlyzr run
   :align: center

   Captured NetAlyzr activity - black shows
   traffic by the packet loss test, red shows
   overall traffic.  No packet loss
   occurred using the replacement switch.

A quick search suggests I'm not the only
one experiencing packet loss issues with
TRENDnet hardware, but nothing particularly
conclusive.  One `reviewer`_ of the same
`faulty switches I purchased`_ did seem to
experience the same problem, but despite this the
product has great reviews overall.  While it's
possible I happened to get two from the same bad
batch, I can't help but wonder if this isn't a
design flaw present in all of these switches.

I have yet to contact TRENDnet about
this issue, but will be attempting
to refund or return the faulty products.
We'll see how that goes :).

Summary
-------

I had previously thought of my unmanaged switches
as incapable of basic failures such as this,
and will more thoroughly research and test
my hardware in the future.

If anyone has any insights that might explain
this behavior, I'm interested and willing
to provide the various packet captures
upon request.  In the meantime, I'll
be contacting TRENDnet about the issue
and looking for a refund or similar.

While these are only two switches, given
the crowded nature of the desktop networking
hardware market I'm going to stay away
from TRENDnet in the future and suggest
others do the same.  Nothing unduly emotional,
but life is too short to risk basic network
components failing in this manner.

Chasing down the issue was a blast, and
I'm glad I can finally play the game
without constantly losing connection to server
in 3+ second bursts.  More importantly,
I solved the puzzle of the strange network
behavior.  Unfortunately now I'll need to find a
new explanation for in-game mistakes! :)

References
----------
.. target-notes::

.. _NetAlyzr: http://netalyzr.icsi.berkeley.edu
.. _buffer bloat: http://www.bufferbloat.net/
.. _initial NetAlyzr results: http://netalyzr.icsi.berkeley.edu/restore/id=36ea240d-2034-f68c2f8d-d5b8-4a3e-8161/
.. _Wireshark: http://www.wireshark.org/
.. _iperf: http://iperf.sourceforge.net/
.. _TRENDnet switches: http://www.amazon.com/gp/product/B001QUA6RA
.. _switches from TP-LINK: http://www.amazon.com/gp/product/B00BZABOTU/
.. _new NetAlyzr results: http://netalyzr.icsi.berkeley.edu/restore/id=36ea240d-8613-5cfd6a62-667e-4a24-b979/
.. _reviewer: http://www.amazon.com/review/R2WV1S555TK8PU/ref=cm_cr_rdp_perm?ie=UTF8&ASIN=B0044GJ516&linkCode=&nodeID=
.. _faulty switches I purchased: http://www.amazon.com/gp/product/B001QUA6RA

