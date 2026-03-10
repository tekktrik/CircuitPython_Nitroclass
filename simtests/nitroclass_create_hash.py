# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for hash functionality."""

from circuitpython_nitroclass import field, nitroclass


@nitroclass(frozen=True)
class DataPacket:
    """Test nitro class."""

    req1 = field(hash=True)
    req2 = field(compare=True)
    req3 = field(hash=False)
    cls_var = "a"


# test_hash
# Tests basic hash functionality.
x = DataPacket(req1=1, req2=2, req3=3)
y = DataPacket(req1=1, req2=2, req3=3)
z = (1, 2)

assert hash(x) == hash(x)
assert hash(x) == hash(y)
assert hash(x) == hash(z)

# test_existing_hash_method
# Tests effect of explicitly setting __hash__ to None.


@nitroclass(frozen=True)
class DataPacket:
    """Test nitro class."""

    req1 = field(hash=True)
    req2 = field(compare=True)
    req3 = field(hash=False)
    cls_var = "a"

    def __hash__(self):  # noqa: D105
        return 42


x = DataPacket(req1=1, req2=2, req3=3)
y = DataPacket(req1=4, req2=5, req3=6)

assert hash(x) == 42  # noqa: PLR2004

assert hash(y) == 42  # noqa: PLR2004

# test_unhashable
# Test setting a class as unhashable.


@nitroclass()
class DataPacket:
    """Test nitro class."""

    req1 = field(hash=True)
    req2 = field(compare=True)
    req3 = field(hash=False)
    cls_var = "a"

    def __hash__(self):  # noqa: D105
        return 42


x = DataPacket(req1=1, req2=2, req3=3)
raises_error = False
try:
    hash(x)
except TypeError:
    raises_error = True
assert raises_error
