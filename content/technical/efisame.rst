``efisame``: Next Boot, Same as This Boot
#########################################

:date: 2015-12-10 16:18
:tags: efi, kernel

`Multi-booting`_ is a widely-used practice that enables a user
to select the OS best suited for their current task.
For example, I dual-boot Windows and Linux on my laptop
which allows me to get the best of both worlds on the same
machine.

I've encountered a minor pain point in this setup however,
largely due to the way I tend to use my machine: once I boot
a particular OS I continue to use that same OS repeatedly and
expect reboots/shutdown/startup to continue to use the last
OS I booted.  This is especially true of reboots, for
example after installing system updates.

Traditionally I addressed this by setting the default boot
to my most-frequently-used OS, but really that is just
optimizing for the common case and not solving the issue.
Additionally, I've recently started using Windows more and
am annoyed having to remind my machine what OS I'm using.

So, today I sat down and put together a simple little
utility to fix this properly once and for all.

PELICAN_END_SUMMARY

Introducing: ``efisame``
========================

This ``efisame`` utility is specifically for systems using `UEFI`_ boot
manager, which is commonly used on hardware made in the last
few years.

What ``efisame`` does is fairly simple, perfoming its task
by manipulating the ``BootNext`` and ``BootCurrent`` EFI
variables.
The ``BootNext`` variable indicates to the EFI boot manager
what to boot from by default for the next boot only.
``BootCurrent`` is read-only and indicates the entry used
to boot the current system.
Together, these form our solution: ``efisame`` tool sets
``BootNext`` to have the value of ``BootCurrent``.
It wraps up with a sanity check for good measure, but
otherwise that's all there is to it.

Running ``efisame`` at Boot
===========================

In order to solve the problem described, ``efisame``
needs to execute every time the system boots.
Any method works here, but since my laptop uses systemd
I created a systemd service file which simply runs the
program on system startup.

Finally, I changed the default EFI boot entry to be Windows
and altogether I now have a system that consistently boots
into the last system I manually indicated I wanted to use.

Available Now
=============

You can get a copy of the utility on the `efisame github`_,
complete with instructions and the systemd service file.

Let me know if you find it useful, or if you have any
problems or questions.

Enjoy!

References
==========
.. target-notes::

.. _Multi-booting: https://en.wikipedia.org/wiki/Multi-booting
.. _UEFI: https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface
.. _efisame github: https://github.com/dtzWill/efi-same
