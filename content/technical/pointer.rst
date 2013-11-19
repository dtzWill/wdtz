Catching pointer overflow bugs
##############################

:date: 2013-11-18 18:05
:tags: overflow, bug, undefined

In all varieties of C/C++, pointer arithmetic is undefined
if it overflows.  That is to say the following example:

.. code-block:: c

  void invalid(char *p) {
    char *q = p + 1;
    printf("%p\n", p - (uintptr_t)q);
  }

invokes undefined behavior as it causes the pointer value to
wraparound to the equivalent of ``-sizeof(char)``, which is
``0xffffffffffffffff`` on my 64bit system.

Unlike integer overflows which can be dangerous or benign
regardless of intention (`ICSE12`_), pointer overflows are very unlikely
to be intentional and may be the source of a more serious
bug resulting in incorrect behavior or program crashing.

Coming Soon To a Clang Near You
-------------------------------

To address this issue I've built an extension to Clang that
checks for pointer overflows (``-fsanitize=pointer-overflow``),
and demonstrate its utility by using it to find bugs in a
variety of popular open source applications.

This will soon be available in mainline Clang as an addition
to the ``-fsanitize=undefined`` set of checks, helping reduce
dangerous occurrences of pointer overflow in the wild.

In the remainder of this post I describe the dangers
of pointer overflow, why existing tools are not
sufficient, and report results from running this tool
on a number of open source applications.

PELICAN_END_SUMMARY


Why Pointer Overflow is Dangerous
---------------------------------

Overflowed pointers can be dangerous in a variety of ways.
The most obvious is that an attempt to deference an
overflowed pointer will likely fail.  These sorts of bugs
are already detected by tools such as valgrind_, asan_, or
SAFECode_.  However these tools are inadequate for vetting
code against pointer overflow in the following ways.

Optimizations Assume No Undefined Behavior
==========================================

Today's compilers are increasingly using optimizations that
assume code does not invoke undefined behavior.  While such
optimizations can be useful (inferring loop bounds, removing
impossible conditions, assertion inference), they can also
cause unexpected and possibly dangerous behavior.  An
example of this is the
`undefined behavior bug in the latest binutils <{filename}../integer/binutils.rst>`_
I've written about previously.  By assuming pointer overflow
cannot occur, the code crashes at runtime due to a removed
"impossible" conditional expression.  Similar optimizations
are performed by many compilers: a table of which compilers
perform which undefined behavior optimizations can be found
in a recent `SOSP'13 paper`_ by Xi Wang, et al (recommended
reading).  These optimizations make the existence of
undefined behavior dangerous beyond the direct impact
of the value computed by the undefined expression.

Unintended Behavior Other Than Crashing
=======================================

Overflowed pointers can result in a variety of undesired
behavior that don't involve dereferencing the result.  For
example, an overflowed pointer might be used to compute an
incorrect offset or used in a comparison that causes
unintended behavior of the program.

Additionally, it's common for data structures (such as
LLVM's DenseMap) to reserve some pointer values
(``-1`` and ``-2``) as special values that are invalid to
use as keys.  Through pointer overflow that generates these
values, the data structure might return the wrong value,
corrupt its data, or crash the program.

Early Detection of Vulnerabilities
==================================
Finally, early detection of pointer overflow can help
fix a potential vulnerability without needing to craft
a full exploit sufficient to trigger a memory safety
or security policy violation.

Together, these make the ability to check index expressions
dynamically for overflow an important part of the testing
process that's not well met by today's tools.

New Sanitizer
-------------
In order to determine how common pointer overflow
is in the wild, I've extended Clang to optionally
add instrumentation to check for pointer overflow
and report any occurrences at runtime.

Clang already has support for adding similar runtime checks
for undefined behavior as part of ``-fsanitize=undefined``,
the spiritual successor of our `IOC (Integer Overflow
Checker) <{filename}../pages/proj/ioc.rst>`_ project.  The new sanitizer is
called ``pointer-overflow``, and will be enabled as part of
``-fsanitize=undefined`` once these features are accepted
upstream, bringing these important checks to the numerous
users already making use of ``-fsanitize=undefined``.

The extension is straightforward: it hooks the various
places Clang generates GEP_ instructions to add
additional code that converts the pointer to an integer
and performs checked arithmetic equivalent to the original
indexing expression.  If the check fails, a call to the
sanitizer runtime is made that reports the error
to the user with a diagnostic similar to the following:

.. raw:: html

  <p><font color="white"><b>./test.c:7:19: <font color="red">runtime error:</font> pointer index expression with base 0x7fffffffd3cb overflowed to 0xffffffffffffffff</b></font></p>

Indicating clearly to the user where in the source
the error occurred, as well as providing relevant
diagnostic information to assist in understanding
what happened so it may be fixed.

Pointer Overflows in the Wild
-----------------------------

To motivate the addition of pointer overflow
checks to Clang, and to justify their inclusion
in ``-fsanitize=undefined``, I built a variety
of open-source software with pointer overflow
checks enabled and ran their test-suites.
I report some of the bugs found below.

Self-Host: Testing LLVM and Clang
=================================

A common practice in compilers is to use
your compiler to build itself, and ensure
the result still works.  As part of testing
the robustness of the pointer overflow sanitizer
I did this, and was surprised to find that while
LLVM did not overflow any pointers, I did
find a bug in Clang's ASTVector_ data structure.

The overflow occurred when attempting to insert
nothing to the end of an empty vector (simplified slightly):

.. code-block:: c++
  
  iterator insert(iterator pos, size_t num, const T &Elt) {
    if (pos == this->end()) {
      append(num, Elt);
      return this->end()-1; // <-- OVERFLOW
    }
    // ...
  }

This occurred most often when attempting to insert the contents
of an empty range into the vector, and occurs regularly
while running Clang's tests.

PCRE 8.33
=========

The latest version of the Perl Compatible Regular Expression (PCRE) library
triggers a pointer overflow in the following code during execution of its test-suite:

.. code-block:: c

  static int
  match_ref(int offset, register PCRE_PUCHAR eptr, int length, match_data *md,
    BOOL caseless)
  {
  PCRE_PUCHAR eptr_start = eptr;
  register PCRE_PUCHAR p = md->start_subject + md->offset_vector[offset];

During execution of the addition in the last line of code.  Interestingly,
the `length` parameter is always negative when this expression overflows,
which results in the function to return before using the dangerous pointer.

While this does not appear to be dangerous currently, there is debug code between
this calculation and the length check that a future change might cause to
use the faulty pointer value, and inlined calls inlined calls to this function
could be broken by compiler optimizations that rely on the assumption that this
is well-defined.

Luckily, this overflow can be easily fixed by moving the later check on
`length` to the function entry, which is my suggested solution.

curl 7.32
=========

This program also overflowed a pointer during execution of its tests,
in particular during Test 138.  Here, a null pointer is decremented
causing the overflow as shown in this excerpt from ``ftp.c``:

.. code-block:: c

  char *bytes;
  bytes=strstr(buf, " bytes");
  if(bytes--) {
    ...
  }

Which overflows when the string "bytes" is not found and ``strstr`` returns
``NULL``.  Because it's invalid to decrement a null pointer, an optimizing
compiler could assume bytes must be non-null and unconditionally execute the
code within.  While I don't know of a compiler that will take advantage of this
as described, but there's no reason to assume this will be true of next year's
compilers.

FFmpeg 2.0.2
============

There was one occurrence of pointer overflow in FFmpeg
while running an instrumented version with its own
FATE test suite:

.. raw:: html

  <p><font color="white"><b>libavcodec/mpegvideo.c:3010:47: <font color="red">runtime error:</font> pointer index expression with base 0x000000000000 overflowed to 0xfffffffffffffff0</b></font></p>

I've not had a chance to fully investigate this yet, but in the past FFmpeg has taken
integer overflow reports seriously and a quick mailing list search suggests they
have interest in purging pointer overflows as well.

php 5.5.5
=========

This software contained multiple pointer overflows.  Two of these are due to expressions
that are evaluated *before* performing checks that abort the function.  These can be easily
resolved by moving the indexing expressions after the safety checks, and are at risk
for an optimizing compiler to break the code as-is.

The other two are in macros ``EX_TMP_VAR`` and ``EX_TMP_VAR_NUM``, which are currently defined
as follows:

.. code-block:: c

  #define EX_TMP_VAR(ex, n)      ((temp_variable*)(((char*)(ex)) + ((int)(n))))
  #define EX_TMP_VAR_NUM(ex, n)  (EX_TMP_VAR(ex, 0) - (1 + (n)))

Which are used to translate between variable index and variable offsets, which
are intentionally negative but unfortunately expressed as pointers instead
of integer values.  These macros can be fixed inplace by replacing with the following
messy equivalents:

.. code-block:: c

  #define EX_TMP_VAR(ex, n)      ((temp_variable*)((zend_uintptr_t)(ex) + sizeof(char)*((int)n)))
  #define EX_TMP_VAR_NUM(ex, n)  ((temp_variable*)((zend_uintptr_t)EX_TMP_VAR(ex, 0) - sizeof(temp_variable)*(1 + (n))))

Which still produces questionably negative pointers, but through casts instead of indexing which
avoids the undefined behavior.  It's likely better to replace these mechanisms altogether
with something cleaner.

Conclusion
----------

Pointer overflow is a common and serious problem that is poorly addressed
by today's tools.  Soon Clang will have support for finding occurrences
of this class of undefined behavior, ready to be used to help
improve the quality of your code.

Enjoy, and happy bug hunting :).

References
----------

.. target-notes::

.. _ICSE12: http://www.cs.utah.edu/~regehr/papers/overflow12.pdf
.. _SOSP'13 paper: http://pdos.csail.mit.edu/papers/stack:sosp13.pdf
.. _valgrind: http://valgrind.org/
.. _asan: http://code.google.com/p/address-sanitizer/
.. _SAFECode: http://safecode.cs.illinois.edu/
.. _GEP: http://llvm.org/docs/GetElementPtr.html
.. _ASTVector: http://lists.cs.uiuc.edu/pipermail/cfe-commits/Week-of-Mon-20131028/091878.html

