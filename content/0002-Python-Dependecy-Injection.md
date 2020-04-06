title: Dependency Injection in Python
date: 2020-04-06
author: me

# Dependency Injection in Python


Dependency inversion is the 'D' in the SOLID principles. It
describes the practice of having class dependencies externally
configured. This enables high-level code to be independent of
low-level code, by each of them depending on an
interface. Depending only on an interface, it is irrelevant from
the perspective of a given class what form the specific
implementation of each of its dependencies has. Since the
behaviour of the class depends on the behaviour of its
dependencies, having the dependencies externally configurable
**inverts control** of the classes behaviour, moving it from the
class itself (constrained by its dependencies) to the class
configurer.

Dependency injection is a common technique which achieves
Dependency Inversion. When using Dependency injection, objects
are constructed with their dependencies by other
objects. Constructor injection and setter injection are the most
common techniques, where the dependencies are passed into the
constructor and a setter method, respectively. In many cases, a
service registry (external configuration) defines a dependency
tree which describes how the application is to construct at
runtime.

In python, dependency inversion capabilities can be achieved
'inline', as it were. Whereas normally you could define some kind
of service registry which instructs the application to construct
with some dependency tree, in Python you can simply define default
values for the injection parameters:
```
    class Printed:
        def get_text(self):
    	print 'foo'
    
    class Printer:
        def __init__(self, dependency: Printed = Printed):
    	self.dependency = dependency()
    
        def execute(self):
    	self.dependency.get_text()
```
As you can see, dependencies can be managed 'inline', and any
given dependency can be swapped out for another at the point of
use.

But what if `Printer` gets passed something unexpected at runtime?

Python's duck-typing is ****roughly**** the same thing as **implicit**
interfaces. If two objects have a method called \`speak()\`, then it
is irrelevant if they explicitly share an interface, because
client code can call the \`speak()\` method, as it expects. There is
an implicit interface which the two \`speak()\`ers both
implement. It may seem utterly strange to static-typing guys, but the
Pythonic way to handle these situations is with a
`try:... except:` block.

In Python 3, you can add typehints to the method signature, which,
in combination with 'inline' dependency injection, and the `abc`
built-in, allows the interface to be explicitly represented and
enforced:
```
    from abc import ABC, abstractmethod
    class Printable(ABC):
        @abstractmethod
        def get_text(self):
    	raise NotImplemented
    
    class PrintedFoo(Printable):
        def get_text(self):
    	return 'foo'
    
    class PrintedBar(Printable):
        def get_text(self):
    	return 'bar'
    
    class Printer:
        def __init__(self, dependency: Printable = PrintedFoo):
    	self.dependency = dependency()
    
        def execute(self):
    	return self.dependency.get_text()  # 'foo'
    
    printer = Printer()
    print(printer.execute())
```
`abc` is the name of a python built-in module and stands for
Abstract Base Class. `abc`'s allow us to define abstract methods
and properties which must be implemented in subclasses.

Making the `Printed` classes each subclasses of `Printable`
enforces implementation of the `get_text` method, and the typehint
on `Printer`'s `__init__` method ensures that the dependency
passed is a `Printable`.

With these two techniques ('inline' dependency injection and
explicit interface declaration), dependency injection in Python is
both rigorous and flexible: dependencies can be managed without
the need of an additional registry, dependencies can be
typehinted, and interfaces can be explicitly enforced.