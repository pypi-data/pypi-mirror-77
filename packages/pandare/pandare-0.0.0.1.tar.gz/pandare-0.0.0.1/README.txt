==========================================
Python Documentation and Releasing Project
==========================================


Introduction
------------

This project is an attempt at documenting Python code and prepare a ready-to-
release Python package, including proper tests and documentations. The ultimate 
goal of this project is to release a Python package of John A. Marohn 
(jam99@cornell.edu) onto GitHub and PyPI.

:Authors: Hoang Long Nguyen
:Email: hn269@cornell.edu

The dummy package
-----------------

This package is literally a dummy package. All it does is adding or subtracting 
two given numbers and give out a result.

Links:
------

ReadTheDocs: https://readthedocs.org/projects/dummy/
GitHub: https://github.com/hn269/dummy/

Quickstart:
-----------

+ At the root document, run ``python setup.py install``.
+ Test the module with ``python setup.py test``.
+ Calling module:
	- ``import dummy``
	- ``result1 = dummy.calc(n1,op,n2)``
	- ``result2 = dummy.calc(n1,op,n2)`` with n1,n2 are numbers, op are operation in string '+','-','*','.' and 'x'
	- ``result3 = dummy.circ(r)`` with r the radius of a circle.

Dependencies:
-------------

jinja 2.7.2 for documentation.
Recommended numpy.

