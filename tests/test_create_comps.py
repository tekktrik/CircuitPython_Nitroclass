# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests comparison functionality."""

import pytest

from circuitpython_nitroclass import field, nitroclass


@nitroclass(order=True)
class DataPacket:
    """Test nitro class."""

    a = field(type=int, priority=2)
    b = field(type=int, priority=1, default=100)


def test_comparisons():
    """Tests basic comparison functionality."""
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
    """Tests attempting comparison between nitro class and other types."""

    @nitroclass(order=True)
    class OtherPacket:
        a = field(type=int, priority=2)
        b = field(type=int, priority=1, default=100)

    x = DataPacket(a=1)
    y = OtherPacket(a=1)

    with pytest.raises(TypeError):
        x < y

    with pytest.raises(TypeError):
        x < 0


def test_nonsequential_priorities():
    """Tests attempting to use nonsequential priorities."""
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


def test_mismatched_compare_priority():
    """Tests that error is raised if compare == False and priority != 0."""
    with pytest.raises(ValueError):

        @nitroclass(order=True)
        class OtherPacket:
            a = field(compare=False, priority=1)


def test_lt_already_defined():
    """Tests that error is raised if __lt__ is already defined."""
    with pytest.raises(TypeError):

        @nitroclass(order=True)
        class DataPacket:
            """Test nitro class."""

            req1 = field(type=int)
            req2 = field(default=5)
            cls_var = "a"

            def __lt__(self, other):
                return True


def test_gt_already_defined():
    """Tests that error is raised if __gt__ is already defined."""
    with pytest.raises(TypeError):

        @nitroclass(order=True)
        class DataPacket:
            """Test nitro class."""

            req1 = field(type=int)
            req2 = field(default=5)
            cls_var = "a"

            def __gt__(self, other):
                return True


def test_le_already_defined():
    """Tests that error is raised if __le__ is already defined."""
    with pytest.raises(TypeError):

        @nitroclass(order=True)
        class DataPacket:
            """Test nitro class."""

            req1 = field(type=int)
            req2 = field(default=5)
            cls_var = "a"

            def __le__(self, other):
                return True


def test_ge_already_defined():
    """Tests that error is raised if __ge__ is already defined."""
    with pytest.raises(TypeError):

        @nitroclass(order=True)
        class DataPacket:
            """Test nitro class."""

            req1 = field(type=int)
            req2 = field(default=5)
            cls_var = "a"

            def __ge__(self, other):
                return True
