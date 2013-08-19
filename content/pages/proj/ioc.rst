Integer Overflow Checker (IOC)
##############################

:date: 2013-08-18
:status: hidden


IOC is the name of the compiler we built for our 2012 ICSE paper
`Understanding Integer Overflow in C/C++`_ that can be used to
check for integer overflows.  IOC extends Clang to add flags to
insert integer overflow check instrumentation, which is useful for catching
bugs or ensuring software operates as expected.

IOC has now been integrated with Clang_ and is can be enabled
with the ``-fsanitize=integer`` flag as of the 3.3 release.


References
----------

.. target-notes::

.. _Understanding Integer Overflow in C/C++: http://www.cs.utah.edu/~regehr/papers/overflow12.pdf
.. _Clang: http://clang.llvm.org/
