# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for frozen (immutability) functionality."""

import pytest

from circuitpython_nitroclass import FrozenInstanceError, field, nitroclass


@nitroclass(frozen=True)
class DataPacket:
    """Test nitro class."""

    req1 = field(type=int)
    req2 = field(default=5)
    cls_var = "a"


def test_frozen():
    """Tests basic nitro class functionality."""
    x = DataPacket(req1=1)

    with pytest.raises(FrozenInstanceError):
        x.req1 = 3

    with pytest.raises(FrozenInstanceError):
        del x.req1

    assert x.req1 == x._req1
    assert x.req2 == x._req2


def test_setattr_defined():
    """Tests attempt to freeze with __setattr__ already defined."""
    with pytest.raises(TypeError):

        @nitroclass(frozen=True)
        class DataPacket:
            """Test nitro class."""

            req1 = field(type=int)
            req2 = field(default=5)
            cls_var = "a"

            def __setattr__(self, name, value):
                return


def test_delattr_defined():
    """Tests attempt to freeze with __delattr__ already defined."""
    with pytest.raises(TypeError):

        @nitroclass(frozen=True)
        class DataPacket:
            """Test nitro class."""

            req1 = field(type=int)
            req2 = field(default=5)
            cls_var = "a"

            def __delattr__(self, name):
                return
