# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests basic nitro class functionality."""

from circuitpython_nitroclass import field, nitroclass


def test_repr():
    """Tests basic nitro class functionality."""

    @nitroclass
    class DataPacket:
        """Test nitro class."""

        req = field(type=int)
        opt = "a"
        dyn = field(default_factory=list)

    x = DataPacket(req=1)
    repr_str = f"y = {repr(x)}"

    locals = {"y": None, "DataPacket": DataPacket}
    exec(repr_str, {}, locals)

    assert x == locals["y"]


def test_not_in_repr():
    """Tests repr implementation when fields are excluded from it."""

    @nitroclass
    class DataPacket:
        """Test nitro class."""

        req = field(default=1, repr=False)
        opt = "a"
        dyn = field(default_factory=list, repr=False)

    x = DataPacket()
    assert repr(x) == "DataPacket(opt='a')"


def test_no_fields():
    """Tests repr implementation when there are no fields given."""

    @nitroclass
    class DataPacket:
        """Test nitro class."""

    x = DataPacket()
    assert repr(x) == "DataPacket()"


def test_no_repr():
    """Tests explicitly turning off repr implementation."""

    @nitroclass(repr=False)
    class DataPacket:
        """Test nitro class."""

    x = DataPacket()
    assert "DataPacket object at 0x" in repr(x)
