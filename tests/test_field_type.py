# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for type checking functionality."""

import pytest

from circuitpython_nitroclass import ValidationError, field, nitroclass


@nitroclass
class DataPacket:
    """Test nitro class."""

    req = field(type=int)
    dyn = field(default_factory=list)
    cls_var = "a"


def test_correct_type():
    """Tests initializing a field with the correct type."""
    _ = DataPacket(req=1)


def test_incorrect_type():
    """Tests initializing a field with the incorrect type."""
    with pytest.raises(ValidationError):
        _ = DataPacket(req="a")
