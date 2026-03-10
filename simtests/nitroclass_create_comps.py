# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests comparison functionality."""

from circuitpython_nitroclass import field, nitroclass


@nitroclass(order=True)
class DataPacket:
    """Test nitro class."""

    a = field(type=int, priority=2)
    b = field(type=int, priority=1, default=100)


# test_comparisons
# Tests basic comparison functionality.
x = DataPacket(a=1)
y = DataPacket(a=1)

assert x <= y
assert x >= y
assert not x < y
assert not x > y

x.a = 2

assert x > y
assert x >= y
assert not x < y
assert not x <= y

x.a = 0

assert x < y
assert x <= y
assert not x > y
assert not x >= y

# test_different_types
# Tests attempting comparison between nitro class and other types.


@nitroclass(order=True)
class OtherPacket:  # noqa: D101
    a = field(type=int, priority=2)
    b = field(type=int, priority=1, default=100)


x = DataPacket(a=1)
y = OtherPacket(a=1)
raises_error = False
try:
    x < y
except TypeError:
    raises_error = True
assert raises_error
raises_error = False
try:
    x < 0
except TypeError:
    raises_error = True
assert raises_error

# test_nonsequential_priorities
# Tests attempting to use nonsequential priorities.
raises_error = False
try:

    @nitroclass(order=True)
    class OtherPacket:  # noqa: D101
        a = field(type=int, priority=2)
        b = field(type=int, priority=3)
        c = field(type=int, priority=4)
except ValueError:
    raises_error = True
assert raises_error
raises_error = False
try:

    @nitroclass(order=True)
    class OtherPacket:  # noqa: D101
        a = field(type=int, priority=1)
        b = field(type=int, priority=2)
        c = field(type=int, priority=4)
except ValueError:
    raises_error = True
assert raises_error
raises_error = False
try:

    @nitroclass(order=True)
    class OtherPacket:  # noqa: D101
        a = field(type=int, priority=1)
        b = field(type=int)
        c = field(type=int, priority=3)
except ValueError:
    raises_error = True
assert raises_error

# test_mismatched_compare_priority
# Tests that error is raised if compare == False and priority != 0.
raises_error = False
try:

    @nitroclass(order=True)
    class OtherPacket:  # noqa: D101
        a = field(compare=False, priority=1)
except ValueError:
    raises_error = True
assert raises_error

# test_lt_already_defined
# Tests that error is raised if __lt__ is already defined.
raises_error = False
try:

    @nitroclass(order=True)
    class DataPacket:
        """Test nitro class."""

        req1 = field(type=int)
        req2 = field(default=5)
        cls_var = "a"

        def __lt__(self, other):  # noqa: D105
            return True
except TypeError:
    raises_error = True
assert raises_error

# test_gt_already_defined
# Tests that error is raised if __gt__ is already defined.
raises_error = False
try:

    @nitroclass(order=True)
    class DataPacket:
        """Test nitro class."""

        req1 = field(type=int)
        req2 = field(default=5)
        cls_var = "a"

        def __gt__(self, other):  # noqa: D105
            return True
except TypeError:
    raises_error = True
assert raises_error

# test_le_already_defined
# Tests that error is raised if __le__ is already defined.
raises_error = False
try:

    @nitroclass(order=True)
    class DataPacket:
        """Test nitro class."""

        req1 = field(type=int)
        req2 = field(default=5)
        cls_var = "a"

        def __le__(self, other):  # noqa: D105
            return True
except TypeError:
    raises_error = True
assert raises_error

# test_ge_already_defined
# Tests that error is raised if __ge__ is already defined.
raises_error = False
try:

    @nitroclass(order=True)
    class DataPacket:
        """Test nitro class."""

        req1 = field(type=int)
        req2 = field(default=5)
        cls_var = "a"

        def __ge__(self, other):  # noqa: D105
            return True
except TypeError:
    raises_error = True
assert raises_error
