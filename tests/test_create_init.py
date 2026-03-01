# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for the init functionality."""

import pytest

from circuitpython_nitroclass import field, nitroclass


@nitroclass
class DataPacket:
    """Test nitro class."""

    req = field(type=int)
    opt = "a"
    dyn = field(default_factory=list)


def test_missing_req_args():
    """Tests missing required arguments during init."""
    with pytest.raises(TypeError):
        _ = DataPacket()


def test_extraneous_args():
    """Tests giving extraneous arguments during init."""
    with pytest.raises(TypeError):
        _ = DataPacket(req=1, nonexistent=42)


def test_duplicate_defaults():
    """Tests using both default and default_factory arguments."""
    with pytest.raises(ValueError):

        @nitroclass
        class BadPacket:
            bad = field(default=3, default_factory=list)


def test_custom_init():
    """Tests using a custom implementation of __init__()."""

    @nitroclass(init=False)
    class OtherPacket:
        attr = field(type=int)

        def __init__(self, reqstr: str) -> None:
            self.attr = int(reqstr)

    x = OtherPacket(reqstr="3")
    assert x.attr == 3  # noqa: PLR2004
