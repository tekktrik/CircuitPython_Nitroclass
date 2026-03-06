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
