# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT
"""
`circuitpython_nitroclass`
================================================================================

Supercharge your CircuitPython classes!


* Author(s): Alec Delaney

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/tekktrik/CircuitPython_nitroclass.git"

from os import fdatasync


def nitroclass(cls):
    def wrap_nitroclass(cls):
        return cls

    return wrap_nitroclass(cls)

sentinel = object()

def add_wacky(*args, **kwargs):

    def cls_add_wacky(cls):
        print(cls)
        print(cls)

        def wrap_add_wacky(*args, **kwargs):

            def dunder_str(self):
                if kwargs.get("yoink", False):
                    return self.a.upper() + "... yoink?"
                return self.a.upper()

            cls.__str__ = dunder_str
            return cls

        if len(args) != 0:
            return wrap_add_wacky(cls)
        return wrap_add_wacky(*args, **kwargs)

    if len(args) == 0:
        return cls_add_wacky
    return cls_add_wacky(args[0])

@add_wacky
class TestClass:

    def __init__(self, a):
        self.a = a

inst = TestClass("haha")
print(str(inst))

