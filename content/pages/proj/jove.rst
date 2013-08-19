JOVE
####

:date: 2013-08-18
:status: hidden

Overview
--------

JOVE (JIT Compilation of the Linux Kernel in a Virtualized
Environment) is a project that enhances SVA_ to JIT compile
the targeted kernel to remove the kernel bytecode itself
from the trusted computing base.  The SVA compiler
instruments the kernel to ensure its safety and that it only
operates using SVA intrinsics to access the hardware.   JOVE
put the SVA compiler into the VMM_ (using hypercalls for the
JIT callbacks) which is not a part of the SVA design, but
both protects the compiler itself and avoids engineering
issues involved in putting a C++ compiler in early kernel
bootstrap code.

Besides use in SVA, JIT compilation of a kernel also enables
a number of optimizations that aren't available statically.

JOVE was a course project for CS498LA (Undergraduate Research Lab).

Related
-------

Poster_

References
----------

.. target-notes::

.. _SVA: http://sva.cs.illinois.edu/
.. _VMM: http://en.wikipedia.org/wiki/Hypervisor
.. _Poster: http://wdtz.org/files/jove_poster.pdf
