# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
#
# SPDX-License-Identifier: MIT
# SPDX-License-Identifier: PSF-2.0
"""Supercharge your CircuitPython classes similar to CPython dataclasses.

* Author(s): Alec Delaney

Implementation Notes
--------------------

**Hardware:**

None

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/tekktrik/CircuitPython_Nitroclass.git"

from collections import namedtuple

from circuitpython_functools import total_ordering


class _MissingSentinel:
    pass


MISSING = _MissingSentinel()

try:
    from typing import Any, Callable, Dict, Self, Type, TypeAlias, TypeVar

    _Missing: TypeAlias = _MissingSentinel
    C = TypeVar("C", bound=type)
except ImportError:  # pragma: no cover
    pass


Field = namedtuple(
    "Field",
    (
        "default_factory",
        "init",
        "repr",
        "hash",
        "compare",
        "priority",
        "type",
        "coerce",
        "validation",
    ),
)


def field(  # noqa: PLR0913
    *,
    default: Any = MISSING,
    default_factory: Callable[[], Any] | _Missing = MISSING,
    init: bool = True,
    repr: bool = True,  # TODO: Implement
    # hash: bool | None = None,  # TODO: Implement
    hash: bool = False,  # TODO: Replace with above
    compare: bool = True,
    priority: int = 0,  # TODO: Implement
    type: Type | _Missing = MISSING,  # TODO: Implement
    coerce: bool = False,  # TODO: Implement
    validation: Callable[[Self, Any], bool] | None = None,  # TODO: Implement
) -> Field:
    """Implement a field for a nitro class."""
    # compare==True, priority==0 >>> __eq__
    # compare==True, priority!=0 >>> __eq__, __gt__, __lt__
    # compare==False, priority==0 >>> none
    # compare==False, priority!=0 >>> ERROR

    # if default != MISSING and default_factory != MISSING:
    if MISSING not in {default, default_factory}:
        raise ValueError("cannot specify both default and default factory")

    if default != MISSING:
        fld_default_factory = lambda: default
    elif default_factory != MISSING:
        fld_default_factory = default_factory
    else:
        fld_default_factory = MISSING

    return Field(
        fld_default_factory,
        init,
        repr,
        hash,
        compare,
        priority,
        type,
        coerce,
        validation,
    )


def _attach_init(cls: C, field_map: Dict[str, Field]) -> None:
    """Attach __init__ method."""
    args_with_defaults = {
        name: fld for name, fld in field_map.items() if fld.default_factory != MISSING
    }
    args_without_defaults = {
        name: fld for name, fld in field_map.items() if fld.default_factory == MISSING
    }

    optional_args = set(args_with_defaults.keys())
    allowed_args = set(name for name, fld in field_map.items() if fld.init)
    required_args = set(args_without_defaults.keys())

    def init_func(self, **args) -> None:  # TODO: Revert to str + exec building?
        # Check if args are missing
        provided_args = set(args.keys())
        if not required_args.issubset(provided_args):
            raise TypeError(
                "Some parameters missing"
            )  # TODO: Expand this error message, match CPython preferably

        # Check that only allowed args were given
        if not provided_args.issubset(allowed_args):
            raise TypeError(
                "Got unexpected keyword argument"
            )  # TODO: Expand error, match CPython?

        # Get args that still require values
        defaulting_args = optional_args.difference(
            provided_args
        )  # TODO: Change to subtraction operator

        # Get the dict for provided values
        provided_dict = {
            name: value for name, value in args.items() if name in provided_args
        }

        # Set provided values
        for name, value in provided_dict.items():
            setattr(self, name, value)

        # Set default values for remaining
        for name in defaulting_args:
            field = field_map[name]
            value = field.default_factory()
            setattr(self, name, value)

    cls.__init__ = init_func


def _attach_repr(cls: C, field_map: Dict[str, Field]) -> None:
    """Attach __repr__ method."""

    def repr_func(self) -> str:
        classname = cls.__qualname__.split(".")[-1]
        repr_str = f"{classname}("
        for name, field in field_map.items():
            if not field.repr:
                continue
            value = repr(getattr(self, name))
            repr_str += f"{name}={value}, "
        if repr_str.endswith(", "):
            repr_str = repr_str[:-2]
        repr_str += ")"
        return repr_str

    cls.__repr__ = repr_func


def _attach_eq(cls: C, field_map: Dict[str, Field]) -> None:
    """Attach __eq__ method."""

    def eq_func(self, value):
        if not isinstance(value, cls):
            raise TypeError(
                "Cannot compare these two classes"
            )  # TODO: Improve error message
        for name, field in field_map.items():
            if field.compare and getattr(self, name) != getattr(value, name):
                return False
        return True

    cls.__eq__ = eq_func


def _attach_comps(cls: C, field_map: Dict[str, Field]) -> None:
    """Attach comparison magic methods."""
    compare_fields = [
        (name, field)
        for name, field in field_map.items()
        if field.compare and field.priority != 0
    ]  # Ignore priority 0
    compare_fields.sort(key=lambda x: x[1].priority)

    given_priorities = [pair[1].priority for pair in compare_fields]
    expected_priorities = list(range(max(given_priorities) + 1))[1:]

    if given_priorities != expected_priorities:
        raise ValueError("Priorities must be given as sequential ints starting from 1")

    def lt_func(self, value):
        if not isinstance(value, cls):
            raise TypeError(
                "Cannot compare these two classes"
            )  # TODO: Improve error message
        for name, _ in compare_fields:
            self_value = getattr(self, name)
            other_value = getattr(value, name)
            if self_value == other_value:
                continue
            return self_value < other_value
        return False

    cls.__lt__ = lt_func

    cls = total_ordering(cls)


def nitroclass(
    cls: C | None = None,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    # unsafe_hash: bool = False,
    # frozen: bool = False,
) -> C:  # noqa
    """Turn the decorated class into a nitro class."""

    def class_wrapper(c):
        arg_names: set[str] = {arg for arg in c.__dict__ if not arg.startswith("__")}

        # Check if arg of type field
        field_map: Dict[str, Field] = {}
        for arg in arg_names:
            val = getattr(c, arg)
            if callable(val):
                continue
            if not isinstance(val, Field):
                val = field(default=val)
            field_map[arg] = val

        if init:
            _attach_init(c, field_map)

        if repr:
            _attach_repr(c, field_map)

        if order and not eq:
            raise ValueError  # TODO: Add message

        if eq:
            _attach_eq(c, field_map)

        if order:
            _attach_comps(c, field_map)

        return c

    if cls is not None:  # kwargs given
        return class_wrapper(cls)

    return class_wrapper
