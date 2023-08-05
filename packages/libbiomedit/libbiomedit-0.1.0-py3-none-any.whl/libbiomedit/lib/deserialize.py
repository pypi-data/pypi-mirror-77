from typing import Union, Tuple, Any, Dict, Optional, Sequence, cast
import collections
import warnings

import dataclasses

from .classify import classify, __origin_attr__, AbstractType, IsDataclass, IsTypingType


def deserialize(T: AbstractType):
    """Creates a deserializer for the type :T:. It handles dataclasses,
    sequences, typing.Optional, Enum and primitive types.

    :returns: A deserializer, converting a dict, list or primitive to :T:
    """
    return _deserializers.get(classify(T), lambda x: x)(T)


_deserializers = {}


def _deserializer(T: Any):
    def decorator(f):
        _deserializers[T] = f
        return f
    return decorator


@_deserializer(Any)
def deserialize_any(_: AbstractType):
    return lambda x: x


@_deserializer(Tuple)
def deserialize_tuple(T: IsTypingType):
    item_types = cast(Tuple[AbstractType, ...], T.__args__)
    if len(item_types) == 2 and item_types[1] is ...:
        item_type = item_types[0]

        def _deserialize_ellipsis(data: tuple):
            return tuple(deserialize(item_type)(item) for item in data)
        return _deserialize_ellipsis

    def _deserialize(data: tuple):
        if len(item_types) != len(data):
            raise ValueError(
                f"Wrong number ({len(data)}) of items for {repr(T)}")
        return tuple(deserialize(T)(item) for T, item in zip(item_types, data))
    return _deserialize


@_deserializer(Sequence)
def deserialize_seq(T: IsTypingType):
    seq_type = getattr(T, __origin_attr__, None)
    try:
        item_type = T.__args__[0]
    except AttributeError:
        raise ValueError(
            f"Sequence of type {seq_type.__name__} without item type")
    if seq_type is collections.abc.Sequence:
        seq_type = list

    def _deserialize(data):
        return seq_type(map(deserialize(item_type), data))
    return _deserialize


@_deserializer(IsDataclass)
def deserialize_dataclass(T):
    fields = dataclasses.fields(T)

    def _deserialize(data):
        unexpected_keys = set(data.keys()) - set(f.name for f in fields)
        if unexpected_keys:
            warnings.warn(
                f"{T.__name__}: Unexpected keys: " +
                ", ".join(unexpected_keys))
        converted_data = {f.name: deserialize(
            get_deserialize_method(f))(data[f.name]) for f in fields
            if f.name in data}
        return T(**converted_data)
    return _deserialize


def get_deserialize_method(f: dataclasses.Field) -> type:
    return f.metadata.get("deserialize", f.type)


@_deserializer(Optional)
def deserialize_optional(T: IsTypingType):
    T1, T2 = T.__args__
    if isinstance(None, T1):
        opt_type = T2
    else:
        opt_type = T1

    def _deserialize(data):
        if data is None:
            return None
        return opt_type(data)
    return _deserialize


@_deserializer(Union)
def deserialize_union(T: IsTypingType):
    types = T.__args__

    def _deserialize(data):
        types_by_name = {t.__name__: t for t in types}
        type_name = data.get("type")
        if type_name is None:
            raise ValueError(
                f"Union[{', '.join(types_by_name)}]: missing `type` item")
        T = types_by_name.get(type_name)
        if T is None:
            raise ValueError(
                f"Union[{', '.join(types_by_name)}]: "
                f"unexpected type `{type_name}`")
        return deserialize(T)(data["arguments"])
    return _deserialize


@_deserializer(Dict)
def deserialize_dict(T: IsTypingType):
    key_type, val_type = T.__args__

    def _deserialize(data):
        return {
            deserialize(key_type)(key): deserialize(val_type)(val)
            for key, val in data.items()}
    return _deserialize
