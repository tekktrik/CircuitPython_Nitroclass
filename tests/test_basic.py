# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests basic nitro class functionality."""

from circuitpython_nitroclass import field, nitroclass


@nitroclass
class DataPacket:
    """Test nitro class."""

    req = field(type=int)
    dyn = field(default_factory=list)
    cls_var = "a"

    def some_method(self) -> int:
        """Square the stored attribute."""
        return self.req**2


def test_basic():
    """Tests basic nitro class functionality."""
    x = DataPacket(req=1)
    y = DataPacket(req=2)

    assert x.req == 1  # noqa: PLR2004
    assert x.dyn == []
    assert x.cls_var == "a"
    assert x != y

    x.req = 2

    assert x.req == 2  # noqa: PLR2004
    assert x.dyn == []
    assert x.cls_var == "a"
    assert x == y
