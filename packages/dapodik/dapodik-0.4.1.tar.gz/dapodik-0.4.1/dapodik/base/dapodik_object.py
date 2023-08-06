from __future__ import annotations
from dataclasses import MISSING
from datetime import datetime, date
from dapodik.config import BASE_URL
from dapodik.utils.helpers import get_dataclass_fields
from dapodik.utils.parser import str_to_datetime, str_to_date

from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from dapodik import Dapodik


class DapodikObject:
    dapodik: Dapodik = None
    _editable: bool = False
    _id: str = ''
    _url: str = ''
    _id_attrs: Tuple[Any, ...] = ()
    _base_url: str = BASE_URL
    _params: Dict[str, str] = {}
    _name: str = ''

    def __post_init__(self):
        self.dapodik.logger.debug('Berhasil membuat {}'.format(
            self.__class__.__qualname__))

    @property
    def id(self):
        return self.__dict__.get(self._id)

    @classmethod
    def from_data(cls,
                  data: dict,
                  id: Optional[str] = None,
                  url: Optional[str] = None,
                  dapodik: Optional[Dapodik] = None,
                  **kwargs) -> DapodikObject:
        fields = get_dataclass_fields(cls)
        safe_data = dict()
        id = id or cls._id

        for field in fields:
            key = field.name
            if key.startswith('_'):
                continue
            value = data.pop(key)

            if value:
                # if hasattr(field.type, 'from_data'):
                #     # safe_data[key] = dapodik[field.type][value]
                if field.type == datetime:
                    safe_data[key] = str_to_datetime(value)
                elif field.type == date:
                    safe_data[key] = str_to_date(value)
                else:
                    safe_data[key] = value
            elif field.default != MISSING:
                safe_data[key] = field.default
            elif field.default_factory != MISSING:
                safe_data[key] = field.default_factory()
            else:
                safe_data[key] = None

        res = cls(**safe_data)

        if id:
            cls._id = id
        if url:
            cls._url = url
        if dapodik:
            cls.dapodik = dapodik
        if kwargs:
            data.update(kwargs)
        if data:
            for key, value in data.items():
                setattr(res, key, value)
        return res

    def to_dict(self) -> dict:
        data = dict()
        for key in self.__dict__:
            if key == 'dapodik' or key.startswith('_'):
                continue
            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value
        return data

    def update(self, data: dict) -> None:
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self) -> str:
        return getattr(self, 'name', self._id)

    def __hash__(self) -> int:
        if self._id_attrs:
            return hash((self.id, self._id_attrs))
        return super().__hash__()

    @property
    def params(self) -> dict:
        return None

    @classmethod
    def get_params(cls) -> dict:
        params = cls._params or {}
        if type(cls.params) == dict:
            params.update(cls.params)
        return params

    @classmethod
    class property:
        "Emulate PyProperty_Type() in Objects/descrobject.c"

        def __init__(self, cls, get_id, update=False, delete=False):
            self.cls: DapodikObject = cls
            self.func = get_id
            self.update = update
            self.delete = False
            self.__doc__ = get_id.__doc__

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            return self.fget(obj)

        def __set__(self, obj, value):
            if self.fset is None:
                raise AttributeError("can't set attribute")
            self.fset(obj, value)

        def __delete__(self, obj):
            if self.fdel is None:
                raise AttributeError("can't delete attribute")
            self.fdel(obj)

        def fget(self, obj: DapodikObject):
            key = self.func(obj)
            do = obj.dapodik[self.cls]
            if not do:
                raise Exception('tidak ditemukan {}'.format(
                    type(self.cls).__qualname__))
            val = do[key]
            if val:
                return val
            raise Exception('id {} tidak ditemukan di {}'.format(
                key,
                type(self.cls).__qualname__))

        def fset(self, obj: DapodikObject, value: Any) -> None:
            key = self.func(obj)
            if self.update:
                c = obj.dapodik[self.cls]
                if c and c[value]:
                    setattr(obj, key, value)
                else:
                    raise ValueError('{} tidak ada di {}'.format(
                        value, self.cls))
            else:
                raise Exception('{} tidak dapat dirubah'.format(
                    self.func.__name__))

        def fdel(self, obj: DapodikObject) -> None:
            key = self.func(obj)
            if self.delete:
                delattr(obj, key)
            else:
                raise Exception("{} tidak dapat dihapus".format(
                    self.func.__name__))
