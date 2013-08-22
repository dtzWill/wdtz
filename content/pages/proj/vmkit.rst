OpenJDK Port of VMKit
#####################

:date: 2013-08-18
:status: hidden


Overview
--------

`VMKit`_ is a VM substrate built on LLVM with functional Java VM and has been used
for CLI, Python, and R.  For improved compatability and to learn the inner
workings of a a language runtime, I ported VMKit to optionally be built
with OpenJDK instead of GNU Classpath.

Status
------

Many things work (eclipse, most of dacapo 2009), but there are still
missing pieces of functionality such as global weak references.

Luckily, it seems the VMKit project has been revived (2012)
in the form of `VMKit2`_ which hopefully further
improves OpenJDK support.

Related
-------

`GitHub Repo`_

`Issue Tracker`_

---------------

References
----------

.. target-notes::

.. _VMKit: http://vmkit.llvm.org/
.. _VMKit2: http://vmkit2.gforge.inria.fr/
.. _GitHub Repo: http://github.com/dtzWill/vmkit
.. _Issue Tracker: http://github.com/dtzWill/vmkit/issues
