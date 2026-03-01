# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT


from circuitpython_nitroclass import field, nitroclass


@nitroclass
class DataPacket:
    req = field(type=int)
    opt = "a"
    dyn = field(default_factory=list)


def test_basic():
    x = DataPacket(req=1)
    y = DataPacket(req=2)

    assert x != y

    x.req = 2

    assert x == y
