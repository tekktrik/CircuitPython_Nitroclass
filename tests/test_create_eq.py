# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for equality functionality."""

import pytest

from circuitpython_nitroclass import field, nitroclass


@nitroclass
class DataPacket:
    """Test nitro class."""

    a = field(type=int)
    b = 100


def test_equality():
    """Tests equality functionality."""
    x = DataPacket(a=1)
    y = DataPacket(a=1)

    assert x == y

    x.a = 2

    assert x != y


def test_different_types():
    """Tests equating nitro class to non-similar type."""

    @nitroclass
    class OtherPacket:
        a = field(type=int)
        b = 100

    x = DataPacket(a=1)
    y = OtherPacket(a=1)

    with pytest.raises(NotImplementedError):
        x == y

    with pytest.raises(NotImplementedError):
        x == 3  # noqa: PLR2004


def test_no_eq():
    """Tests opting out of equality functionality."""

    @nitroclass(eq=False)
    class OtherPacket:
        """Test nitro class."""

        a = field(type=int)
        b = 100

    x = OtherPacket(a=1)
    y = OtherPacket(a=1)

    assert x != y


def test_eq_order_mismatch():
    """Tests preventing using eq=False and order=True together."""
    with pytest.raises(ValueError):

        @nitroclass(eq=False, order=True)
        class OtherPacket:
            a = field(type=int)
            b = 100
