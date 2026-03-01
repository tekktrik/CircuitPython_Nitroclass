# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: Unlicense

import pytest

from circuitpython_nitroclass import field, nitroclass


@nitroclass
class DataPacket:
    req = field(type=int)
    opt = "a"
    dyn = field(default_factory=list)


def test_missing_req_args():
    with pytest.raises(TypeError):
        _ = DataPacket()


def test_extraneous_args():
    with pytest.raises(TypeError):
        _ = DataPacket(req=1, nonexistent=42)


def test_duplicate_defaults():
    with pytest.raises(ValueError):

        @nitroclass
        class BadPacket:
            bad = field(default=3, default_factory=list)


def test_custom_init():
    @nitroclass(init=False)
    class OtherPacket:
        attr = field(type=int)

        def __init__(self, reqstr: str) -> None:
            self.attr = int(reqstr)

    x = OtherPacket(reqstr="3")
    assert x.attr == 3
