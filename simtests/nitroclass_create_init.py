# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for init functionality."""

from circuitpython_nitroclass import field, nitroclass


@nitroclass
class DataPacket:
    """Test nitro class."""

    req = field(type=int)
    dyn = field(default_factory=list)
    cls_var = "a"


# test_missing_req_args
# Tests missing required arguments during init.
raises_error = False
try:
    _ = DataPacket()
except TypeError:
    raises_error = True
assert raises_error

# test_extraneous_args
# Tests giving extraneous arguments during init.
raises_error = False
try:
    _ = DataPacket(req=1, nonexistent=42)
except TypeError:
    raises_error = True
assert raises_error

# test_duplicate_defaults
# Tests using both default and default_factory arguments.
raises_error = False
try:

    @nitroclass
    class BadPacket:  # noqa: D101
        bad = field(default=3, default_factory=list)
except ValueError:
    raises_error = True
assert raises_error


# test_custom_init
# Tests using a custom implementation of __init__().
@nitroclass(init=False)
class OtherPacket:  # noqa: D101
    attr = field(type=int)

    def __init__(self, reqstr: str) -> None:  # noqa: D107
        self.attr = int(reqstr)


x = OtherPacket(reqstr="3")
assert x.attr == 3  # noqa: PLR2004
