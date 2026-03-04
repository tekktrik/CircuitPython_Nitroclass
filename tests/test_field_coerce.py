# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for type coercion functionality."""

import pytest

from circuitpython_nitroclass import ValidationError, field, nitroclass


@nitroclass
class DataPacket:
    """Test nitro class."""

    req = field(type=int, coerce=True)
    dyn = field(default_factory=list)
    cls_var = "a"


def test_correct_type():
    """Tests initializing a field with the correct type."""
    _ = DataPacket(req=1)


def test_incorrect_type_correct_value():
    """Tests initializing a field with the incorrect type but correct value."""
    _ = DataPacket(req="1")


def test_incorrect_type_incorrect_value():
    """Tests initializing a field with the incorrect type and incorrect value."""
    with pytest.raises(ValidationError):
        _ = DataPacket(req="a")


def test_coerce_but_no_type():
    """Tests initializing a field with no type but coerce=True."""
    with pytest.raises(ValueError):

        @nitroclass
        class DataPacket:
            """Test nitro class."""

            req = field(coerce=True)
            dyn = field(default_factory=list)
            cls_var = "a"
