# abc-delegation

[![Codeship Status for monomonedula/abc-delegation](https://app.codeship.com/projects/5be7b410-92cb-0138-678c-1680fac8559a/status?branch=master)](https://app.codeship.com/projects/400234)
[![codecov](https://codecov.io/gh/monomonedula/abc-delegation/branch/master/graph/badge.svg)](https://codecov.io/gh/monomonedula/abc-delegation)
[![PyPI version](https://badge.fury.io/py/abc-delegation.svg)](https://badge.fury.io/py/abc-delegation)

A tool for automated delegation with abstract base classes.

This metaclass enables creation of delegating classes 
inheriting from an abstract base class. 

This technique is impossible with regular `__getattr__` approach for delegation,
so normally, you would have to define every delegated method explicitly.
Not any more

The metaclasses also enable optional validation of the delegate attributes
to ensure they have all of the methods required by the parent object.

### Installation:
`pip install abc-delegation`


### Basic usage:
```python    
from abc import ABCMeta

from abc_delegation import delegation_metaclass

class A(metaclass=ABCMeta):
    @abstractmethod
    def bar(self):
        pass

    @abstractmethod
    def foo(self):
        pass

class B:
    def bar(self):
        return "B bar"

    def foo(self):
        return "B foo"

class C(A, metaclass=delegation_metaclass("my_delegate")):
    def __init__(self, b):
        self.my_delegate = b

    def foo(self):
        return "C foo"

c = C(B())
assert c.foo() == "C foo"
assert c.bar() == "B bar"
```

### Validation
```python
class A(metaclass=ABCMeta):
    @abstractmethod
    def bar(self):
        pass

    @abstractmethod
    def foo(self):
        pass

class B:
    pass

# validation is on by default
class C(A, metaclass=delegation_metaclass("_delegate")):
    def __init__(self, b):
        self._delegate = b

    def foo(self):
        return "C foo"

C(B())
# Trying to instantiate C class with B delegate which is missing 'bar' method
# Validation raises an error:
# TypeError: Can't instantiate bar: missing attribute bar in the delegate attribute _delegate
```


### Multiple delegates:
```python
from abc import ABCMeta

from abc_delegation import multi_delegation_metaclass


class A(metaclass=ABCMeta):
    @abstractmethod
    def bar(self):
        pass

    @abstractmethod
    def foo(self):
        pass

    @abstractmethod
    def baz(self):
        pass

class B:
    def bar(self):
        return "B bar"

    def foo(self):
        return "B foo"

class X:
    def baz(self):
        return "X baz"

class C(A, metaclass=multi_delegation_metaclass("_delegate1", "_delegate2")):
    def __init__(self, d1, d2):
        self._delegate1 = d1
        self._delegate2 = d2

    def foo(self):
        return "C foo"

c = C(B(), X())
assert c.bar() == "B bar"
assert c.foo() == "C foo"
assert c.baz() == "X baz"
```

Please refer to the unit tests for more examples.
