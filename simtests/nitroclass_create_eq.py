# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for equality functionality."""

from circuitpython_nitroclass import field, nitroclass


@nitroclass
class DataPacket:
    """Test nitro class."""

    a = field(type=int)
    b = 100


# test_equality
# Tests equality functionality.
x = DataPacket(a=1)
y = DataPacket(a=1)

assert x == y

x.a = 2

assert x != y

# test_different_types
# Tests equating nitro class to non-similar type.


@nitroclass
class OtherPacket:  # noqa: D101
    a = field(type=int)
    b = 100


x = DataPacket(a=1)
y = OtherPacket(a=1)
raises_error = False
try:
    x == y
except TypeError:
    raises_error = True
assert raises_error
raises_error = False
try:
    x == 3  # noqa: PLR2004
except TypeError:
    raises_error = True
assert raises_error

# test_no_eq
# Tests opting out of equality functionality.


@nitroclass(eq=False)
class OtherPacket:
    """Test nitro class."""

    a = field(type=int)
    b = 100


x = OtherPacket(a=1)
y = OtherPacket(a=1)

assert x != y

# test_eq_order_mismatch
# Tests preventing using eq=False and order=True together.
raises_error = False
try:

    @nitroclass(eq=False, order=True)
    class OtherPacket:  # noqa: D101
        a = field(type=int)
        b = 100
except ValueError:
    raises_error = True
assert raises_error

# test_eq_exists
# Tests if an explicit implementation of __eq__ already exists.


@nitroclass
class OtherPacket:  # noqa: PLW1641, D101
    a = field(type=int)

    def __eq__(self, value):  # noqa: D105
        return False


x = OtherPacket(a=100)

assert x != x  # noqa: PLR0124
