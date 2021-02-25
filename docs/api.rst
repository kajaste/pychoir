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
.. autoclass:: InAnyOrder
.. autoclass:: IsEmpty
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
.. autofunction:: that
.. autoclass:: pychoir.core.MatcherWrapper
   :members:

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
.. autoclass:: MatcherLike
   :members:
   :undoc-members:

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
.. autoclass:: MatchesRegex
.. autoclass:: StartsWith

Types
-----
.. autoclass:: ConvertsTo
.. autoclass:: IsInstance
.. autoclass:: OfType
