title: Python Standard Library
date: 2020-07-06
author: Harry
category: development

- [Python Standard Library](#orge64dc58)
  - [Built-In Functions](#org0922c8a)
    - [`abs(x)`](#orgb71adf0)
    - [`all(iterable)`](#org03ee61b)


<a id="orge64dc58"></a>

# Python Standard Library


<a id="org0922c8a"></a>

## Built-In Functions


<a id="orgb71adf0"></a>

### `abs(x)`

> Return the absolute value of a number. The argument may be an integer or a floating point number. If the argument is a complex number, its magnitude is returned.

```python
print(abs(1))
print(abs(-1))
print(abs(1.0))
print(abs(-1.0))

print(abs(2+3j))
```

Turns out you can use `j` after a number in Python to denote a complex number. Didn't know that before today!


<a id="org03ee61b"></a>

### `all(iterable)`

> Return True if all elements of the iterable are true (or if the iterable is empty).

```python
print(all([True, True, True]))
print(all([False, False, False]))
print(all([]))
print(all([True, True, False]))
print(all([1, 1, 1]))
print(all([1, 1, None]))
print(all([None, None, None]))
print(all([]) == bool([]))
```

I find it a little weird that `all([])` evaluates to `True`, since `[]` is falsey.