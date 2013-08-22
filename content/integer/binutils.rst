Undefined Behavior in Binutils Causes Segfault
##############################################

:date: 2013-08-19 14:24
:tags: integer, bug, binutils, undefined


As reported on the `binutils bugzilla`_.

No response yet, but should be easy to fix.

Details follow (same as in bug report but easier to read).

PELICAN_END_SUMMARY

Description
-----------

The file ``tc-i386-intel.c`` contains undefined behavior in
recent binutils versions (including latest at time of
writing).

The error occurs in multiple places
(for example `line 432`_, reproduced below) and is incorrect
as it assumes unsigned integer wrapping semantics for
pointer arithmetic on the variable ``scale`` in a number of
places.  In particular, the check:

.. code-block:: c

 432           if (ret && scale && (scale + 1))

Gets optimized to ``if (ret && scale)`` because it is impossible for ``scale + 1`` to evaluate to ``NULL`` without invoking undefined behavior.  Note that the earlier decrement from ``NULL`` is also invalid, and possibly other constructs in related code.

This is is a problem as it results in the conditional being taken when scale is ``(int*)-sizeof(int)``, which leads to an invalid pointer being dereferenced in ``resolve_expression()``.


Steps to reproduce
------------------

1) Obtain and unpack binutils 2.22 or latest via git (tested with 0b0b7b5).
2) Obtain clang 3.3 or latest trunk (from your package manager or build) and modify PATH as appropriate.
3) Configure similar to the following:

.. code-block:: sh

  $ CC=clang CXX=clang++ ./configure --disable-werror --enable-ld=no

4) Build.

.. code-block:: sh

  $ make -j

5) Run the just-built 'as' using the following program from the testsuite:

.. code-block:: sh

  $ valgrind gas/as-new --32 gas/testsuite/gas/i386/intelbad.s

6) Observe segfault, see referenced `valgrind.log`_ for the output of the above command.


Impact
------

Presently prevents building a functional binutils with recent versions of
clang, and is a time-bomb for breaking future builds.  Compilers (including gcc
and clang) are known to increasingly take advantage of undefined behavior in
newer versions and so this may be an issue in the future even with
compilers/platforms that safely build this today.


valgrind.log
------------

Valgrind log from step #5 above:

.. _valgrind.log:



::

  ==80032== Memcheck, a memory error detector
  ==80032== Copyright (C) 2002-2011, and GNU GPL'd, by Julian Seward et al.
  ==80032== Using Valgrind-3.8.0.SVN and LibVEX; rerun with -h for copyright info
  ==80032== Command: gas/as-new --32 gas/testsuite/gas/i386/intelbad.s
  ==80032== 

  ...

  ==80032== Invalid read of size 8
  ==80032==    at 0x40D881: resolve_expression (expr.c:2026)
  ==80032==    by 0x42EA9F: i386_intel_simplify (tc-i386-intel.c:415)
  ==80032==    by 0x42E8A2: i386_intel_simplify (tc-i386-intel.c:297)
  ==80032==    by 0x42E5F7: i386_intel_simplify (tc-i386-intel.c:297)
  ==80032==    by 0x427835: md_assemble (tc-i386-intel.c:537)
  ==80032==    by 0x415E1E: read_a_source_file (read.c:950)
  ==80032==    by 0x404606: main (as.c:1089)
  ==80032==  Address 0xffffffffffffffe0 is not stack'd, malloc'd or (recently) free'd
  ==80032== 
  ==80032== 
  ==80032== Process terminating with default action of signal 11 (SIGSEGV)
  ==80032==  Access not within mapped region at address 0xFFFFFFFFFFFFFFE0
  ==80032==    at 0x40D881: resolve_expression (expr.c:2026)
  ==80032==    by 0x42EA9F: i386_intel_simplify (tc-i386-intel.c:415)
  ==80032==    by 0x42E8A2: i386_intel_simplify (tc-i386-intel.c:297)
  ==80032==    by 0x42E5F7: i386_intel_simplify (tc-i386-intel.c:297)
  ==80032==    by 0x427835: md_assemble (tc-i386-intel.c:537)
  ==80032==    by 0x415E1E: read_a_source_file (read.c:950)
  ==80032==    by 0x404606: main (as.c:1089)
  ==80032==  If you believe this happened as a result of a stack
  ==80032==  overflow in your program's main thread (unlikely but
  ==80032==  possible), you can try to increase the size of the
  ==80032==  main thread stack using the --main-stacksize= flag.
  ==80032==  The main thread stack size used in this run was 10485760.
  ==80032== 
  ==80032== HEAP SUMMARY:
  ==80032==     in use at exit: 3,931,677 bytes in 1,740 blocks
  ==80032==   total heap usage: 1,894 allocs, 154 frees, 3,963,363 bytes allocated
  ==80032== 
  ==80032== LEAK SUMMARY:
  ==80032==    definitely lost: 0 bytes in 0 blocks
  ==80032==    indirectly lost: 0 bytes in 0 blocks
  ==80032==      possibly lost: 0 bytes in 0 blocks
  ==80032==    still reachable: 3,931,677 bytes in 1,740 blocks
  ==80032==         suppressed: 0 bytes in 0 blocks
  ==80032== Rerun with --leak-check=full to see details of leaked memory
  ==80032== 
  ==80032== For counts of detected and suppressed errors, rerun with: -v
  ==80032== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 4 from 4)

---------------

References
----------
.. target-notes::

.. _binutils bugzilla: http://sourceware.org/bugzilla/show_bug.cgi?id=15836
.. _line 432: http://sourceware.org/git/?p=binutils.git;a=blob;f=gas/config/tc-i386-intel.c;h=3f6b057613451839c796ca8a9cdbef2fe6532ec6;hb=HEAD#l432
