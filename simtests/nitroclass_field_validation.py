# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for validation functionality."""

from circuitpython_nitroclass import ValidationError, field, nitroclass


@nitroclass
class DataPacket:
    """Test nitro class."""

    def validate_req(self, value):
        """Validate the required input."""
        return value > self.cls_var

    req = field(validation=validate_req)
    dyn = field(default_factory=list)
    cls_var = 10


# test_valid
# Tests initializing a field with a valid value.
_ = DataPacket(req=100)

# test_incvalid
# Tests initializing a field with an invalid value.
raises_error = False
try:
    _ = DataPacket(req=1)
except ValidationError:
    raises_error = True
assert raises_error
