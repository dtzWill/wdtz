Kernel hacking: My very own BSOD
#################################

:date: 2013-09-24 15:58
:tags: kernel, freebsd, bsod

While working on hacking the FreeBSD kernel
for a research project, I of course have
crashed things many times.  Hooray for VM's.

However, this latest time I've managed to really
mess things up.  Instead of some esoteric message
in the logs, the result was the following being
written to the console:

.. figure:: /images/kernel_wut.png
   :alt: nonsense kernel console output
   :align: center

   Nonsense Kernel console output

Hopefully those of you who've hacked on kernels previously
will appreciate the "wut" moment you get when your screen
looks like this instead of acting as expected :).

PELICAN_END_SUMMARY
