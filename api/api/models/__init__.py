"""
Base model of DB object
"""

import time
from abc import abstractmethod
from typing import Union, Optional, Any, Callable
from copy import deepcopy

from ..funcs.mongodb import db


def _next_id(name):
    """ Next DB ID """

    id_last = list(db[name].find({}, {'id': True, '_id': False}).sort('id', -1))

    if id_last:
        return id_last[0]['id'] + 1

    return 1

def pre_process_created(cont):
    if isinstance(cont, int):
        return float(cont)

    return cont


class Attribute:
    """ Descriptor """

    name: str = None
    types: Any = None
    default: Any = None
    checking: Callable = None
    pre_processing: Callable = None
    processing: Callable = None

    def __init__(
        self,
        types,
        default=None,
        checking=None,
        pre_processing=None,
        processing=None,
    ):
        self.types = types
        self.default = default
        self.checking = checking
        self.pre_processing = pre_processing
        self.processing = processing

    def __set_name__(self, instance, name):
        self.name = name

    def __get__(self, instance, owner):
        if not instance:
            if isinstance(self.default, Callable):
                return self.default(owner)
            else:
                return deepcopy(self.default)

        if self.name in instance.__dict__:
            return instance.__dict__[self.name]

        if self.default is not None:
            if isinstance(self.default, Callable):
                instance.__dict__[self.name] = self.default(instance)
            else:
                instance.__dict__[self.name] = deepcopy(self.default)

            return instance.__dict__[self.name]

        return None

    def __set__(self, instance, value) -> None:
        if self.pre_processing:
            value = self.pre_processing(value)

        if not isinstance(value, self.types):
            raise TypeError(self.name)

        if self.checking and not self.checking(instance.id, value):
            raise ValueError(self.name)

        if self.processing:
            value = self.processing(value)

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

# pylint: disable=C0103,R0913
class Base:
    """ Base model """

    id = Attribute(types=int, default=0) # TODO: unique
    name = Attribute(types=str) # TODO: required
    created = Attribute(types=float, pre_processing=pre_process_created)
    status = Attribute(types=int)

    @property
    @abstractmethod
    def _db(self) -> str:
        """ Database name """

    def __init__(self, data: dict = None, **kwargs) -> None:
        # Auto complete (instead of Attribute(auto=...))
        self.created = time.time()

        if not data:
            data = kwargs

        for name, value in data.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        if not hasattr(self, name):
            raise AttributeError('key')

        super().__setattr__(name, value)

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        setattr(self, name, value)

    def _is_default(self, name):
        """ Check the value for the default value """

        data = deepcopy(self)
        delattr(data, name)

        return getattr(self, name) == getattr(data, name)

    @classmethod
    def get(
        cls,
        ids: Union[list[int], int, None] = None,
        fields: Union[list[str], tuple[str], set[str], None] = None,
        search: Optional[str] = None, # TODO
        count: Optional[int] = None,
        offset: int = 0,
        **kwargs,
    ):
        """ Get instances of the object """

        process_one = False

        if ids:
            if isinstance(ids, int):
                process_one = True
                db_condition = {
                    'id': ids,
                }
            else:
                db_condition = {
                    'id': {'$in': ids},
                }
        else:
            db_condition = {}

        if kwargs:
            for arg in kwargs:
                db_condition[arg] = kwargs[arg]

        db_filter = {
            '_id': False,
        }

        if fields:
            for value in fields:
                db_filter[value] = True

        els = db[cls._db].find(db_condition, db_filter)
        els = els.sort('id', -1)

        last = count + offset if count else None
        els = els[offset:last]

        els = [cls(el) for el in els]

        if process_one:
            return els[0]

        return els

    def save(
        self,
    ):
        """ Save the instance """

        # TODO: auto values
        # TODO: deleting values

        # Edit
        if self.id:
            db[self._db].update_one(
                {'id': self.id},
                {'$set': self.json(default=False)},
            )

            return

        # Create
        self.id = _next_id(self._db)
        db[self._db].insert_one(self.json(default=False))

    def json(
        self,
        default=True, # Return default values
        fields=None,
    ):
        """ Get dictionary of the object """
        """
        If default is True and there are fields, it will return only fields with
        non-default values
        """

        data = {}

        for attr in dir(self):
            if fields and attr not in fields:
                continue

            if attr[0] == '_' or callable(getattr(self, attr)):
                continue

            if not default and self._is_default(attr):
                continue

            data[attr] = getattr(self, attr)

        return data
