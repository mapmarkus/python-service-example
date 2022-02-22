import logging
import enum
import json


LOG_LEVEL_DICT = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'error': logging.ERROR,
}


def get_log_level(name):
    """Get log level by name

        >>> get_log_level('debug')
        10
    """
    return LOG_LEVEL_DICT.get(name.lower(), logging.ERROR)


class Select(str, enum.Enum):
    """Special Enum that can be used with pydantic to serialize and unserialize using
    strings

    Use Enum Functional API to create new instances:

        >>> Fruit = Select('Fruit', ['apple', 'orange', 'pear'])
        >>> Fruit.apple
        <Fruit.apple: 'Apple'>
        >>> Fruit('Pear')
        <Fruit.pear: 'Pear'>
    """

    def _generate_next_value_(name, *args):
        return name.title()


class IntSelect(int, enum.Enum):
    """Special Enum that can be used with pydantic to serialize and unserialize using
    ints. Is the same as IntEnum, but this sets the names automatically from a list of
    strings.

    **Note**: Numbers must use the prefix '_'

    Use Enum Functional API to create new instances:

        >>> Speed = IntSelect('Speed', ['_100', '_200', '_300'])
        >>> Speed._100
        <Speed._100: 100>
        >>> Speed(200)
        <Speed._200: 200>
    """
    def _generate_next_value_(name, *args):
        return name[1:]


def safe_dict_json_loads(raw):
    """Transform a string to json (dict) safely

    If loading json fails, `{}` is returned instead of raising an exception.

        >>> safe_json_loads('')
        {}
        >>> safe_json_loads('not a dict')
        {}
        >>> safe_json_loads(None)
        {}
        >>> safe_json_loads('{"x": 1}')
        {'x': 1}
    """
    if raw:
        try:
            return json.loads(raw)
        except Exception:
            pass

    return {}


def safe_dict_json_dumps(data):
    """Transform data to a string safely

    If data is not a dict, or dumping fails, `'{}'` is returned instead of raising an
    exception.

        >>> safe_json_dumps('')
        '{}'
        >>> safe_json_dumps('not json')
        '{}'
        >>> safe_json_dumps(None)
        '{}'
        >>> safe_json_dumps({'x': 1})
        '{"x": 1}'
    """
    if isinstance(data, dict):
        try:
            return json.dumps(data)
        except Exception:
            pass

    return '{}'
