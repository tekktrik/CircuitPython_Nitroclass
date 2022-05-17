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
