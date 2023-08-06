Demonstration of an idea:
# Signature Dependent Semantics

There are two goals to the proposal:
1. Maintain nearly all backward compatibility for all item dunder methods even when using the 
`signature_dependent_semantics` decorator.

    ```python
    >>> from sigdepsem import signature_dependent_semantics as sds
    >>> @sds
    ... class C:
    ...     def __init__(self, name):
    ...         self.name = name
    ...     def __getitem__(self, key):
    ...         return f"{(*key,)}"
    ...     def __setitem__(self, key, value):
    ...         self.set = f"{self.name}[{(*key,)}] = {value}"
    ...     def __delitem__(self, key):
    ...         self.del_ = f"del {self.name}[{(*key,)}]"
    ... 
    >>> C("c")[1,2,3]
    '(1, 2, 3)'
    ```

2. Allow for an optional change to the semantic meaning of the signatures of `__getitem__`, 
`__setitem`, `__delitem__` such that the semantic meaning is more consistent with regular 
function calls.
    
    Example:

    ```python
    >>> from sigdepsem import signature_dependent_semantics as sds
    >>> @sds
    ... class MyMapping:
    ...    # note the unusual __getitem__ signature that looks more like the
    ...    # signature of a regular callable (3 positional arguments)
    ...    def __getitem__(self, a, b, c):
    ...        return a, b, c
    ... 
    >>> 
    >>> m = MyMapping()
    >>> 
    >>> m[1,2,3]
    (1, 2, 3)
    >>> m[1,2,3,4]
    ...
    TypeError: __getitem__() takes 4 positional arguments but 5 were given
    ```
