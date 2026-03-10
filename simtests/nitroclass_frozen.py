# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for frozen (immutability) functionality."""

from circuitpython_nitroclass import FrozenInstanceError, field, nitroclass


@nitroclass(frozen=True)
class DataPacket:
    """Test nitro class."""

    req1 = field(type=int)
    req2 = field(default=5)
    cls_var = "a"


# test_frozen
# Tests basic nitro class functionality.
x = DataPacket(req1=1)
raises_error = False
try:
    x.req1 = 3
except FrozenInstanceError:
    raises_error = True
assert raises_error
raises_error = False
try:
    del x.req1
except FrozenInstanceError:
    raises_error = True
assert raises_error

assert x.req1 == x._req1
assert x.req2 == x._req2

# test_setattr_defined
# Tests attempt to freeze with __setattr__ already defined.
raises_error = False
try:

    @nitroclass(frozen=True)
    class DataPacket:
        """Test nitro class."""

        req1 = field(type=int)
        req2 = field(default=5)
        cls_var = "a"

        def __setattr__(self, name, value):  # noqa: D105
            return
except TypeError:
    raises_error = True
assert raises_error

# test_delattr_defined
# Tests attempt to freeze with __delattr__ already defined.
raises_error = False
try:

    @nitroclass(frozen=True)
    class DataPacket:
        """Test nitro class."""

        req1 = field(type=int)
        req2 = field(default=5)
        cls_var = "a"

        def __delattr__(self, name):  # noqa: D105
            return
except TypeError:
    raises_error = True
assert raises_error
