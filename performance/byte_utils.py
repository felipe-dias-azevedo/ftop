from enum import Enum


def get_byte_type(value):
    value_type = value
    metric = "Bytes/s"
    if 1_000 <= value < 1_000_000:
        value_type = to_kilo(value)
        metric = "KiB/s"
    elif value >= 1_000_000:
        value_type = to_mega(value)
        metric = "MiB/s"
    return {"value": value_type, "metric": metric}


class TypeByteLength(Enum):
    KILO, MEGA, GIGA = range(0, 3)


def convert_length(byte_type, value, rounded):
    power = 0
    if byte_type == TypeByteLength.KILO:
        power = 10
    elif byte_type == TypeByteLength.MEGA:
        power = 20
    elif byte_type == TypeByteLength.GIGA:
        power = 30
    value_converted = value / (2 ** power)
    if rounded:
        return round(value_converted, 2)
    return value_converted


def to_kilo(value, rounded=False):
    return convert_length(TypeByteLength.KILO, value, rounded)


def to_mega(value, rounded=False):
    return convert_length(TypeByteLength.KILO, value, rounded)


def to_giga(value, rounded=False):
    return convert_length(TypeByteLength.KILO, value, rounded)
