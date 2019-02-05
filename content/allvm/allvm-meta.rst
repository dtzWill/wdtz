A few more ALLVM tidbits are now available
###########################################

:date: 2019-02-04
:tags: allvm, llvm, research, release

Posted on the ALLVM github organization,
the `allvm-meta` repository is now available--
and because naming is hard it ended up being
the repository with perhaps the least "meta" content.

Even so I'm excited to make this public
and will give a brief overview below.

PELICAN_END_SUMMARY

ALLVM Logo
----------

Based on the LLVM logo, this contribution was made by the
especially talented `Richard Wei`_ and the resulting graphics
have been used in many places and I'm really thankful for the work.

I'm fond of it and you can find it on the `ALLVM website`_,
on my slide templates, the `ALLVM GitHub Organization`_,
and more places.

There's even a favicon for use on our `Hydra`_ ALLVM CI server--
not publicly available yet because disk failures complicated the migration
but is likely to be revived on new public hosting soon,
as more of the ALLVM bits go public.

LLVM JIT in the BSD Kernel
--------------------------

ALLVM researches systems where ALL code is available as IR,
and in the "big picture" plan this included the kernel as well as userspace
with the compiler as a first-class component of the OS.

In this little code dump are most of the bits I used for my exploratory
blitz towards getting an LLVM JIT as close to the metal as I could
manage in a few weeks.

Unfortunately some of the patches for uclibc, uclibc++, and LLVM
have been lost-- but when I get a free weekend I think they're
in an old backup but it'll take some work to dig through that.

Even so this is the work that caused the `fun BSOD`_ I posted
about at the time: as I recall I did something like scribbled
LLVM IR all over system memory due to a silly mistake.

My solution was to shove enough of an LLVM JIT and hacked "runtime" support
into a bsd kernel module that hopefully the bootloader or early
kernel init could host.

This worked well enough that I was able to point it at bitcode
for the FreeBSD kernel and successfully codegen the result.

It couldn't quite execute the result, although I THINK that
was largely a matter of rejiggering a number of things to
pivot into it gracefully--  not because the code was wrong.

I'll hopefully find those pieces soon,
and might not be ready for exploring but it's
at least in a better place than it was :).

I wrote an email to the ALLVM co-founders
my advisor Vikram and `Joshua Cranmer`_,
which is a nice piece of "history"
and the early excitement of the project!

You'll find it in the allvm-meta repo,
it describes my goals and status better
than the summary above.

Here: `ALLVM JIT Status Email`_

References
----------
.. target-notes::

.. _allvm-meta: https://github.com/allvm/allvm-meta
.. _Richard Wei: https://twitter.com/rxwei
.. _ALLVM website: http://allvm.org
.. _ALLVM GitHub Organization: https://github.com/allvm
.. _hydra: https://nixos.org/hydra
.. _fun BSOD: {filename}../technical/kernel_wut.rst
.. _Joshua Cranmer: http://quetzalcoatal.blogspot.com/
.. _ALLVM JIT Status Email: https://raw.githubusercontent.com/allvm/allvm-meta/master/bsd_kernel/ALLVM-Status-update
