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


def nitroclass(*args, **kwargs):

    def wrapper_nitroclass(cls):

        def modifier_nitroclass(*args, **kwargs):

            # Add functionality based on arguments provided

            # Add __init__
            if kwargs.get("init", False):

                def dunder_init(self, *args, **kwargs):
                    for arg  # TODO: WIP

            # Add __repr__
            if kwargs.get("repr", False):

                def dunder_repr(self):
                    return self.a.upper() + "... yoink?"

                cls.__repr__ = dunder_repr


            return cls

        if len(args) == 0:
            return modifier_nitroclass(*args, **kwargs)
        return modifier_nitroclass(cls)

    if len(args) == 0:
        return wrapper_nitroclass
    return wrapper_nitroclass(args[0])

@
class TestClass:

    def __init__(self, a):
        self.a = a

inst = TestClass("haha")
print(str(inst))

