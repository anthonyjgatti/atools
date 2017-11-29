#!/bin/python3

"""This file uses a few abstract concepts that allow the class API to build up
state via repeated method calls. To do this, we make use of a Generative base class
and implement a fluent interface, as a opposed to have method calls continually
return self. This is a technique to allow a.method1().method2() type calls.

Some references:
https://stackoverflow.com/questions/36250990/return-self-in-python
https://github.com/zzzeek/sqlalchemy/blob/master/lib/sqlalchemy/sql/base.py

"""

import functools

class Generative(object):
    """Allow a child instance to generate itself via the @_generative decorator."""

    def _generate(self):
        s = self.__class__.__new__(self.__class__)
        s.__dict__ = self.__dict__.copy()
        return s


def _generative(func):
    """Mark a method as generative."""

    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        generated_self = self._generate()
        func(generated_self, *args, **kwargs)
        return generated_self

    return decorator
