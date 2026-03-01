# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: Unlicense

import pytest

from circuitpython_nitroclass import field, nitroclass


@nitroclass
class DataPacket:
    a = field(type=int)
    b = 100


def test_equality():
    x = DataPacket(a=1)
    y = DataPacket(a=1)

    assert x == y

    x.a = 2

    assert x != y


def test_different_types():
    @nitroclass
    class OtherPacket:
        a = field(type=int)
        b = 100

    x = DataPacket(a=1)
    y = OtherPacket(a=1)

    with pytest.raises(NotImplementedError):
        x == y


def test_no_eq():
    @nitroclass(eq=False)
    class OtherPacket:
        a = field(type=int)
        b = 100

    x = OtherPacket(a=1)
    y = OtherPacket(a=1)

    assert x != y


def test_eq_order_mismatch():
    with pytest.raises(ValueError):

        @nitroclass(eq=False, order=True)
        class OtherPacket:
            a = field(type=int)
            b = 100
