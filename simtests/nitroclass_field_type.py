# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for type checking functionality."""

from circuitpython_nitroclass import ValidationError, field, nitroclass


@nitroclass
class DataPacket:
    """Test nitro class."""

    req = field(type=int)
    dyn = field(default_factory=list)
    cls_var = "a"


# test_correct_type
# Tests initializing a field with the correct type.
_ = DataPacket(req=1)

# test_incorrect_type
# Tests initializing a field with the incorrect type.
raises_error = False
try:
    _ = DataPacket(req="a")
except ValidationError:
    raises_error = True
assert raises_error
