from enum import Enum


def to_dict(obj):
    if (isinstance(obj, Enum)):
        return obj.name
    if (isinstance(obj, dict)):
        data = {}
        for key in obj:
            data[key] = to_dict(obj[key])
        return data
    if (isinstance(obj, list)):
        return [to_dict(v) for v in obj]
    if (hasattr(obj, "__dict__")):
        data = dict()
        for key in obj.__dict__:
            value = obj.__dict__[key]
            if (value is not None):
                data[key] = to_dict(value)
        return data
    return obj
