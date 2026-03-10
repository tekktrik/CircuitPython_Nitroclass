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
HIDDEN_PREFIX = "_"

try:
    from typing import Any, Callable, Dict, Self, Type, TypeAlias, TypeVar

    _Missing: TypeAlias = _MissingSentinel
    C = TypeVar("C", bound=type)
except ImportError:  # pragma: no cover
    pass


class FrozenInstanceError(AttributeError):
    """Exception raised when attempting to modify frozen instances."""


class ValidationError(Exception):
    """Exception raised when failing to validate or coerce a field."""


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
    repr: bool = True,
    hash: bool | None = None,
    compare: bool = True,
    priority: int = 0,
    type: Type | _Missing = MISSING,
    coerce: bool = False,
    validation: Callable[[Self, Any], bool] | None = None,
) -> Field:
    """Implement a field for a nitro class."""
    # compare==True, priority==0 >>> __eq__
    # compare==True, priority!=0 >>> __eq__, __gt__, __lt__
    # compare==False, priority==0 >>> none
    # compare==False, priority!=0 >>> ERROR

    if MISSING not in {default, default_factory}:
        raise ValueError("cannot specify both default and default factory")

    if default != MISSING:
        fld_default_factory = lambda: default
    elif default_factory != MISSING:
        fld_default_factory = default_factory
    else:
        fld_default_factory = MISSING

    create_hash = hash or (hash is None and compare)

    return Field(
        fld_default_factory,
        init,
        repr,
        create_hash,
        compare,
        priority,
        type,
        coerce,
        validation,
    )


def _attach_init(cls: C, field_map: Dict[str, Field], frozen: bool) -> None:
    """Attach __init__ method."""
    optional_fields = {
        name: fld for name, fld in field_map.items() if fld.default_factory != MISSING
    }
    required_fields = {
        name: fld for name, fld in field_map.items() if fld.default_factory == MISSING
    }

    optional_args = set(optional_fields.keys())
    allowed_args = set(name for name, fld in field_map.items() if fld.init)
    required_args = set(required_fields.keys())

    def init_func(self, **args) -> None:  # TODO: Revert to str + exec building?
        # Check if args are missing
        provided_args = set(args.keys())
        if frozen:
            provided_args = {HIDDEN_PREFIX + name for name in provided_args}
        if not required_args.issubset(provided_args):
            missing_args = provided_args - required_args
            raise TypeError(f"Missing parameters: {missing_args}")

        # Check that only allowed args were given
        if not provided_args.issubset(allowed_args):
            unexpected_args = allowed_args - provided_args
            raise TypeError(f"Got unexpected keyword arguments: {unexpected_args}")

        # Get args that still require values
        defaulting_args = optional_args - provided_args

        # Get the dict for provided values
        provided_dict = {}
        for name, value in args.items():
            provided_dict[name] = value

        # Set provided values
        for name, value in provided_dict.items():
            full_name = HIDDEN_PREFIX + name if frozen else name

            # Only validate provided args
            set_value = value
            field = field_map[full_name]
            if field.type != MISSING and not isinstance(set_value, field.type):
                if field.coerce:
                    try:
                        set_value = field.type(value)
                    except ValueError as err:
                        raise ValidationError(
                            f"could not coerce field {name} to type {field.type}"
                        ) from err
                else:
                    raise ValidationError(f"field {name} is not of type {field.type}")
            if field.validation is not None and not field.validation(self, set_value):
                raise ValidationError(f"could not validate field {name}")
            setattr(self, full_name, set_value)

        # Set default values for remaining
        for full_name in defaulting_args:
            field = field_map[full_name]
            value = field.default_factory()
            setattr(self, full_name, value)

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
    if cls.__dict__.get("__eq__", None):
        return cls

    def eq_func(self, value):
        if not isinstance(value, cls):
            raise TypeError(
                f"Cannot compare these two classes: {self.__class__} and {value.__class__}"
            )
        for name, field in field_map.items():
            if field.compare and getattr(self, name) != getattr(value, name):
                return False
        return True

    cls.__eq__ = eq_func


def _attach_comps(cls: C, field_map: Dict[str, Field]) -> None:
    """Attach comparison magic methods."""
    has_lt = cls.__dict__.get("__lt__", None)
    has_gt = cls.__dict__.get("__gt__", None)
    has_le = cls.__dict__.get("__le__", None)
    has_ge = cls.__dict__.get("__ge__", None)

    if has_lt or has_gt or has_le or has_ge:
        raise TypeError("Comparison functions already defined.")

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
                f"Cannot compare these two classes: {self.__class__} and {value.__class__}"
            )
        for name, _ in compare_fields:
            self_value = getattr(self, name)
            other_value = getattr(value, name)
            if self_value == other_value:
                continue
            return self_value < other_value
        return False

    cls.__lt__ = lt_func

    cls = total_ordering(cls)


def _make_immutable(cls: C, field_map: Dict[str, Field]) -> None:
    """Make the instance immutable."""
    has_setattr = cls.__dict__.get("__setattr__", None)
    has_delattr = cls.__dict__.get("__delattr__", None)

    if has_setattr or has_delattr:
        raise TypeError("__setattr__ or __delattr__ already defined")

    for name in field_map:
        property_name = name[1:]

        def prop_getter(self, name=name):
            return getattr(self, name)

        def prop_setter(self, value):
            raise FrozenInstanceError("Cannot change frozen instances")

        def prop_deleter(self):
            raise FrozenInstanceError("Cannot delete from frozen instances")

        prop = property(prop_getter, prop_setter, prop_deleter)

        prop = prop.setter(prop_setter)

        setattr(cls, property_name, prop)


def _attach_hash(cls: C, field_map: Dict[str, Field]) -> None:
    """Attach __hash__ method."""
    if cls.__dict__.get("__hash__", None):
        return cls

    iter_list = [(name, field) for name, field in field_map.items() if field.hash]
    iter_list.sort(key=lambda x: x[0])

    def hash_func(self):
        attr_list = []
        for name, _ in iter_list:
            attr_list.append(getattr(self, name))
        return hash(tuple(attr_list))

    cls.__hash__ = hash_func


def _make_unhashable(cls: C) -> None:

    def unhashable_func(self):
        raise TypeError(f"this class is not hashable")

    cls.__hash__ = unhashable_func


def nitroclass(  # noqa: PLR0913
    cls: C | None = None,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
) -> C:
    """Turn the decorated class into a nitro class."""

    def class_wrapper(c):  # noqa: PLR0912
        arg_names: set[str] = {arg for arg in c.__dict__ if not arg.startswith("__")}

        # Check if arg of type field
        field_map: Dict[str, Field] = {}
        for arg in arg_names:
            val = getattr(c, arg)
            if callable(val):
                continue
            if not isinstance(val, Field):
                continue
            full_arg = HIDDEN_PREFIX + arg if frozen else arg
            field_map[full_arg] = val

        mismatched = {
            field
            for field in field_map.values()
            if field.type == MISSING and field.coerce
        }
        if mismatched:
            raise ValueError("Cannot have fields with no types but coerce=True")

        mismatched = {
            field
            for field in field_map.values()
            if not field.compare and field.priority != 0
        }
        if mismatched:
            raise ValueError(
                "Cannot have fields with compare == False and priority != 0"
            )

        if init:
            _attach_init(c, field_map, frozen)

        if repr:
            _attach_repr(c, field_map)

        if order and not eq:
            raise ValueError("Cannot have order=True and eq=False")

        if eq:
            _attach_eq(c, field_map)

        if order:
            _attach_comps(c, field_map)

        if frozen:
            _make_immutable(c, field_map)

        if (eq and frozen) or unsafe_hash:
            _attach_hash(c, field_map)
        elif eq:
            _make_unhashable(c)  # Implementation raises TypeError

        return c

    if cls is not None:  # kwargs given
        return class_wrapper(cls)

    return class_wrapper
