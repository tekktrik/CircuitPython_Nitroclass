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
