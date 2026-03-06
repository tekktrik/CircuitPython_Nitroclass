# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: Unlicense

"""Example file showing usage of nitroclass library."""

from circuitpython_nitroclass import field, nitroclass


@nitroclass
class DataPacket:
    """Example nitro class."""

    req = field(type=int)
    dyn = field(default_factory=list)
    cls_var = "a"


x = DataPacket(req=1)
y = DataPacket(req=2)

assert x != y

x.req = 2

assert x == y
