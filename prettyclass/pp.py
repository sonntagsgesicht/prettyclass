# -*- coding: utf-8 -*-

# prettyclass
# -----------
# pretty classes - pretty easy.  (created by auxilium)
#
# Author:   sonntagsgesicht
# Version:  0.1, copyright Monday, 07 October 2024
# Website:  https://github.com/sonntagsgesicht/prettyclass
# License:  Apache License 2.0 (see LICENSE file)


from inspect import stack, signature
from json import loads, dumps
from os import linesep as _sep
from typing import Type


def _init_super(cls: Type):
    parameters = []
    for k, p in signature(cls).parameters.items():
        if k == 'self':
            continue
        match p.kind:
            case 1:
                parameters.append(k)
            case 2:
                parameters.append('*' + k)
            case 3:
                parameters.append(k + '=' + k)
            case 4:
                parameters.append('**' + k)
    return f"__init__({' ,'.join(parameters)})"


def _add_init(cls: Type):
    # build __init__ as source code text
    sig = signature(cls.__init__)
    s = [f"def __init__{sig}:"]
    s += [f"    self.{p} = {p}" for p in sig.parameters if not p == 'self']
    s += [f"    _super(self).{_init_super(cls)}"]

    # set state and build function
    _globals = {'_super': lambda self: super(cls, self)}
    exec(_sep.join(s), _globals, _globals)  # nosec B102

    # And finally create the class.
    qualname = getattr(cls, '__qualname__', None)
    cls_doc = getattr(cls, '__doc__', None)
    init_doc = getattr(cls.__init__, '__doc__', None)

    # create subclass (similar to datasclasse._add_slots)
    cls_dict = dict(cls.__dict__)
    cls_dict['__init__'] = _globals.get('__init__')
    cls = type(cls)(cls.__name__, (cls,), cls_dict)

    if qualname is not None:
        cls.__qualname__ = qualname
    if cls_doc is not None:
        cls.__doc__ = cls_doc
    if init_doc is not None:
        cls.__init__.__doc__ = init_doc

    return cls


def _add_slots(cls, is_frozen=False):
    # Need to create a new class, since we can't set __slots__
    #  after a class has been created.

    # Make sure __slots__ isn't already set.
    if '__slots__' in cls.__dict__:
        raise TypeError(f'{cls.__name__} already specifies __slots__')

    # Create a new dict for our new class.
    cls_dict = dict(cls.__dict__)
    field_names = tuple(f for f in signature(cls).parameters)
    cls_dict['__slots__'] = field_names
    for field_name in field_names:
        # Remove our attributes, if present. They'll still be
        #  available in _MARKER.
        cls_dict.pop(field_name, None)

    # Remove __dict__ itself.
    cls_dict.pop('__dict__', None)

    # And finally create the class.
    qualname = getattr(cls, '__qualname__', None)
    cls = type(cls)(cls.__name__, cls.__bases__, cls_dict)
    if qualname is not None:
        cls.__qualname__ = qualname

    # _dataclass_getstate and _dataclass_setstate
    # are needed for pickling frozen
    # classes with slots.  These could be slightly
    # more performant if we generated
    # the code instead of iterating over fields.
    # But that can be a project for
    # another day, if performance becomes an issue.
    def _dataclass_getstate(self):
        return [getattr(self, f) for f in field_names]

    def _dataclass_setstate(self, state):
        for field, value in zip(field_names, state):
            # use setattr because dataclass may be frozen
            object.__setattr__(self, field, value)

    if is_frozen:
        # Need this for pickling frozen classes with slots.
        cls.__getstate__ = _dataclass_getstate
        cls.__setstate__ = _dataclass_setstate

    return cls


def _fields(self):
    s = signature(self.__class__)
    kpv = ((k, p, getattr(self, k, p.default))
           for k, p in s.parameters.items())
    return {k: v for k, p, v in kpv if not v == p.default}


def _bound_arguments(self):
    # scan attributes used as arguments
    s = signature(self.__class__)
    kpv = ((k, p, getattr(self, k, p.default))
           for k, p in s.parameters.items())
    kv = {k: v for k, p, v in kpv if not v == p.default}
    # use function name rather than repr string
    # kv = {k: getattr(v, '__qualname__', v) for k, v in kv.items()}
    b = s.bind(**kv)
    args, kwargs = b.args, b.kwargs

    var_p = [k for k, v in b.signature.parameters.items() if v.kind == 2]
    if 1 < len(var_p):
        raise RuntimeError('found more than one var positional argument')
    var_p = kwargs.pop(var_p[0], ()) if var_p else ()
    args += var_p

    var_kw = [k for k, v in b.signature.parameters.items() if v.kind == 4]
    if 1 < len(var_kw):
        raise RuntimeError('found more than one var keyword only argument')
    var_kw = kwargs.pop(var_kw[0], {}) if var_kw else {}
    kwargs.update(var_kw)

    return args, kwargs


def _setstate(self, state):
    for p, v in state.items():
        setattr(self, p, v)


def _default(self):
    return self.__json__() if hasattr(self, '__json__') else repr(self)


def _dumps(self):
    """dump instance to json via signature arguments pretty easy"""
    args, kwargs = _bound_arguments(self)
    args = [getattr(a, '__qualname__', a) for a in args]
    kwargs = {k: getattr(v, '__qualname__', v) for k, v in kwargs.items()}
    d = self.__class__.__qualname__, args, kwargs
    return dumps(d, indent=2, default=_default)


def _loads(s, globals=()):
    globals = globals or globals()
    d = loads(s)
    if not isinstance(d, (list, tuple)):
        raise ValueError("no valid object structure found")
    if len(d) == 3:
        # ['PrettyClass', [1, 2, 3], {'a': 0}]
        cls, args, kwargs = d
    elif len(d) == 2:
        # ['PrettyClass', [1, 2, 3]]
        cls, args = d
        kwargs = {}
        if isinstance(args, dict):
            # ['PrettyClass', {'a': 0}]
            args, kwargs = [], args
    else:
        raise ValueError("no valid object structure found")

    cls = globals.get(cls)

    # replace existing global objects like functions or classes
    # or _load PrettyClasses
    def update(k, v, container):
        if isinstance(v, str) and v in globals:
            # replace existing global objects
            container[k] = globals.get(v)
        if (isinstance(v, list) and v and v[0] in globals) or \
                (isinstance(v, dict) and 'type' in a and v['type'] in globals):
            # _load PrettyClasses
            try:
                container[k] = _loads(v, globals)
            except ValueError:
                pass

    for i, a in enumerate(args):
        update(i, a, args)
    for k, v in kwargs.items():
        update(k, v, kwargs)

    return cls(*args, **kwargs)


def _from_json(cls, s):
    """load instance from json via signature arguments pretty easy"""
    objs = globals()
    objs[cls.__qualname__] = cls
    return _loads(s, globals=objs)


def _copy(self):
    """copy instance via signature arguments pretty easy"""
    args, kwargs = _bound_arguments(self)
    return self.__class__(*args, **kwargs)


def _eq(self, other):
    """compares instance via signature arguments pretty easy"""
    args, kwargs = _bound_arguments(self)
    orgs, kworgs = _bound_arguments(other)
    return (all(a == o for a, o in zip(args, orgs)) and
            all(kwargs[k] == kworgs[k] for k in set(kwargs).union(kworgs)))


def _bool(self):
    """decides bool value of instance via signature arguments pretty easy"""
    args, kwargs = _bound_arguments(self)
    return all(map(bool, args)) and all(map(bool, kwargs.values()))


def _hash(self):
    """hash instance via signature arguments pretty easy"""
    return hash(repr(self.__dict__))


def _r(self):
    return str if any(f.function == '__str__' for f in stack()) else repr


def _pp(self, *, r=None, sep=', '):
    r = r or _r(self)
    args, kwargs = _bound_arguments(self)
    args = [getattr(a, '__qualname__', r(a)) for a in args]
    kwargs = {k: getattr(v, '__qualname__', r(v)) for k, v in kwargs.items()}
    params = [f"{a}" for a in args] + [f"{k}={v}" for k, v in kwargs.items()]
    return f"{self.__class__.__qualname__}({sep.join(params)})"


def _repr(self):
    """repr instance via signature arguments pretty easy"""
    return _pp(self, r=repr)


def _str(self):
    """str instance via signature arguments pretty easy"""
    return _pp(self, r=str)


def _process(cls, init, repr, copy, eq, nonzero, hash, json):
    if init:
        cls = _add_init(cls)
    if repr:
        setattr(cls, '__str__', _str)
        setattr(cls, '__repr__', _repr)
    if copy:
        setattr(cls, '__copy__', _copy)
        setattr(cls, '__setstate__', _setstate)
    if eq:
        setattr(cls, '__eq__', _eq)
    if nonzero:
        setattr(cls, '__bool__', _bool)
    if hash:
        setattr(cls, '__hash__', _hash)
    if json:
        setattr(cls, '__json__', _dumps)
        setattr(cls, 'from_json', classmethod(_from_json))
    return cls


def prettyclass(cls: Type = None, *, init: bool = True, repr: bool = True,
                copy: bool = True, eq: bool = False, nonzero: bool = False,
                hash: bool = False, json: bool = False):
    """pretty class decorator

    Returns the same class as was passed in, with dunder methods
    added based on the fields defined in the '__init__' signature .

    :param cls: class to add methods
    :param init: add '__init__' method body
        by storing all arguments of its signature,
        so they are available for the added methods
        but are not needed to be implemented
        (optional; default is **True**)
    :param repr: bool to add '__repr__' and '__str__'
        (optional; default is **True**)
    :param copy: bool to add '__copy__'
        as well as ability to pickle
        (optional; default is **True**)
    :param eq: bool to add '__eq__'
        which then returns **True** if all arguments fields are equal
        (optional; default is **False**)
    :param nonzero: bool to add '__bool__'
        which then returns **True** if all arguments fields are **True**
        (optional; default is **False**)
    :param hash: bool to add '__hash__'
        which then returns `hash(repr(self.__dict__))`
        (optional; default is **False**)
    :param json: bool to add '__json__' and classmethod 'from_json'
        to serialize and de-serialize json strings
        (optional; default is **False**)
    :return: same class

    It is recommended to avoid any further attributes
    which define the state of an instance.
    Otherwise, the instance replication would not be ensured.

    >>> from prettyclass import prettyclass

    >>> @prettyclass()
    ... class ABC:
    ...     def __init__(self, a, *b, c, d=1, e, **f):
    ...         '''creates ABC instance'''

    The decorator adds automaticly all argument fields as attributes.

    >>> abc = ABC(1, 2, [3, 4], c=5, d=6, e=7, g='A', h='B')
    >>> abc.__dict__
    {'a': 1, 'b': (2, [3, 4]), 'c': 5, 'd': 6, 'e': 7, 'f': {'g': 'A', 'h': 'B'}}

    >>> abc.a, abc.b, abc.c, abc.d, abc.e, abc.f
    (1, (2, [3, 4]), 5, 6, 7, {'g': 'A', 'h': 'B'})

    and returns a pretty nice representation of an instance

    >>> abc
    ABC(1, 2, [3, 4], c=5, d=6, e=7, g='A', h='B')

    Note the difference between 'str' and 'repr'

    >>> str(abc)
    'ABC(1, 2, [3, 4], c=5, d=6, e=7, g=A, h=B)'

    >>> repr(abc)
    "ABC(1, 2, [3, 4], c=5, d=6, e=7, g='A', h='B')"

    Copy works by default, too.

    >>> from copy import copy
    >>> copy(abc)
    ABC(1, 2, [3, 4], c=5, d=6, e=7, g='A', h='B')

    Same for pickle.

    >>> from pickle import dumps, loads
    >>> s = dumps(abc)  # doctest: +SKIP
    >>> loads(s)  # doctest: +SKIP
    ABC(1, 2, [3, 4], c=5, d=6, e=7, g='A', h='B')

    Note, the string representation ommitts entries
    which coincide with defaults

    >>> ABC(1, 2, [3, 4], c=5, d=1, e=7, g='A', h='B')
    ABC(1, 2, [3, 4], c=5, e=7, g='A', h='B')

    """ # noqa E501
    def wrap(cls):
        return _process(cls, init, repr, copy, eq, nonzero, hash, json)
    # See if we're being called as @dataclass or @dataclass().
    if cls is None:
        # We're called with parens.
        return wrap
    # We're called as @dataclass without parens.
    return wrap(cls)
