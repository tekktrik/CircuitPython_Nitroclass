# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: Unlicense

import pytest

from circuitpython_nitroclass import field, nitroclass


@nitroclass(order=True)
class DataPacket:
    a = field(type=int, priority=2)
    b = field(type=int, priority=1, default=100)


def test_comparisons():
    x = DataPacket(a=1)
    y = DataPacket(a=1)

    assert x <= y
    assert x >= y
    assert not x < y
    assert not x > y

    x.a = 2

    assert x > y
    assert x >= y
    assert not x < y
    assert not x <= y

    x.a = 0

    assert x < y
    assert x <= y
    assert not x > y
    assert not x >= y


def test_different_types():
    @nitroclass(order=True)
    class OtherPacket:
        a = field(type=int, priority=2)
        b = field(type=int, priority=1, default=100)

    x = DataPacket(a=1)
    y = OtherPacket(a=1)
    with pytest.raises(NotImplementedError):
        x < y


def test_nonsequential_priorities():
    # Not starting from 1
    with pytest.raises(ValueError):

        @nitroclass(order=True)
        class OtherPacket:
            a = field(type=int, priority=2)
            b = field(type=int, priority=3)
            c = field(type=int, priority=4)

    # Skipping
    with pytest.raises(ValueError):

        @nitroclass(order=True)
        class OtherPacket:
            a = field(type=int, priority=1)
            b = field(type=int, priority=2)
            c = field(type=int, priority=4)

    # Skipping
    with pytest.raises(ValueError):

        @nitroclass(order=True)
        class OtherPacket:
            a = field(type=int, priority=1)
            b = field(type=int)
            c = field(type=int, priority=3)
