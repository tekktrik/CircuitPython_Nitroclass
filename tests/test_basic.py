# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: Unlicense

"""Tests basic nitro class functionality."""

from circuitpython_nitroclass import field, nitroclass


@nitroclass
class DataPacket:
    """Test nitro class."""

    req = field(type=int)
    opt = "a"
    dyn = field(default_factory=list)

    def some_method(self) -> int:
        """Square the stored attribute."""
        return self.req**2


def test_basic():
    """Tests basic nitro class functionality."""
    x = DataPacket(req=1)
    y = DataPacket(req=2)

    assert x != y

    x.req = 2

    assert x == y
