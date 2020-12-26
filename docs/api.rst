.. module:: pychoir

API Reference
=============

Comparisons
-----------
.. autoclass:: EqualTo
.. autoclass:: GreaterThan
.. autoclass:: GreaterThanOrEqualTo
.. autoclass:: LessThan
.. autoclass:: LessThanOrEqualTo
.. autoclass:: NotEqualTo
.. autoclass:: EQ
.. autoclass:: GT
.. autoclass:: GTE
.. autoclass:: LT
.. autoclass:: LTE
.. autoclass:: NE

Containers
----------
.. autoclass:: All
.. autoclass:: AreNot
.. autoclass:: ContainsAllOf
.. autoclass:: ContainsAnyOf
.. autoclass:: ContainsNoneOf
.. autoclass:: DictContainsAllOf
.. autoclass:: HasLength
.. autoclass:: IsNotPresentOr
.. autoclass:: Len
.. autoattribute:: containers.NotPresent

Core
----
.. autoclass:: Matchable
   :members: __eq__
.. autoclass:: Matcher
   :members:
   :private-members:

Existential
-----------
.. autoclass:: Anything
.. autoclass:: In
.. autoclass:: Is
.. autoclass:: IsFalsy
.. autoclass:: IsNoneOr
.. autoclass:: IsTruthy
.. autoclass:: OneOf
.. autoclass:: Optionally

Integration
-----------
.. autoclass:: Matches
.. autoclass:: M

Logical
-------
.. autoclass:: AllOf
.. autoclass:: And
.. autoclass:: AnyOf
.. autoclass:: IsNoneOf
.. autoclass:: Not
.. autoclass:: Or
.. autoclass:: ResultsTrueFor

Strings
-------
.. autoclass:: EndsWith
.. autoclass:: StartsWith

Types
-----
.. autoclass:: IsInstance
.. autoclass:: OfType
