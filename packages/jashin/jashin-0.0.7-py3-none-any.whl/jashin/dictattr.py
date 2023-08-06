from __future__ import annotations

from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

from .omit import OMIT

__all__ = ("ItemAttr", "MappingAttr", "SequenceAttr", "DictModel")


F = TypeVar("F")
Loader = Callable[[Any], F]
Dumper = Callable[[F], Any]


class ItemAttrBase(Generic[F]):
    funcs: Tuple[Optional[Loader[F]], Optional[Dumper[F]]]
    name: Optional[str]
    DICT_METHOD: str = "__dictattr_get__"

    def __init__(
        self,
        load: Optional[Loader[F]] = None,
        dump: Optional[Dumper[F]] = None,
        *,
        name: Optional[str] = None,
        default: Any = OMIT,
    ):

        # save loader/dumper as tuple to prevent descr functionary
        self.funcs = (load, dump)
        self.name = name
        self.default = default

    def __set_name__(self, owner: Any, name: str) -> None:
        if self.name is None:
            self.name = name

    def _get_dict(self, instance: Any) -> Dict[str, Any]:
        f = getattr(instance, self.DICT_METHOD, None)
        if not f:
            raise TypeError(
                f"{instance.__class__.__qualname__} does not provide"
                f"`{self.DICT_METHOD}` method."
            )

        return cast(Dict[str, Any], f())

    def _get_value(self, instance: Any, owner: type) -> Tuple[Optional[Loader[F]], Any]:
        """ Get value from dict"""

        data = self._get_dict(instance)

        if self.name not in data:
            if self.default is not OMIT:
                return None, cast(F, self.default)
            raise ValueError(f"{self.name} is not found")

        return self.funcs[0], data[self.name]

    def _dump_value(self, value: Any) -> Any:
        dumper = self.funcs[1]
        if dumper:
            return dumper(value)

        f = getattr(value, self.DICT_METHOD, None)
        if f:
            return f()

        return value

    def _set(self, instance: Any, value: Any) -> None:
        assert self.name, "Field name is not provided"
        data = self._get_dict(instance)

        value = self._dump_value(value)
        data[self.name] = value

    def __delete__(self, instance: Any) -> None:
        data = self._get_dict(instance)
        assert self.name, "Field name is not provided"
        del data[self.name]


class ItemAttr(ItemAttrBase[F]):
    """Define an attribute to access an item of the source dictionary.

    :param load: Convert value from the source dictionary item.
    :param dump: Convert assigned value to store to the source dictionary item.
    :param name: key in the source dictionary item. Default to attr name in class.
    :param default: Default value is the item is not exit in the source dictionary.

    ItemAttr get value from the dictionary obtained from self.__dictattr_get__()
    method of the class. The key to retrieve value from the dictionary is the name
    of attribute. If ``name`` is specified, it is used as the key instead.

    ``load`` is a function with a single argument. If specified, ``load`` is called
    on read acess on the attribute to convert value in the dictionary.

    ``dump`` is a function with a single argument. If specified, ``dump`` is called
    on write acess on the attribute to convert value to be stored to the dictionary.
    If the ``dump`` is not specified and the value assigned to has ``__dictattr_get__``
    method, the result of ``__dictattr_get__()`` method is stored to the dictionary.

    ``default`` is the value used if the key is not exist on the source dictionary.

    """

    def __get__(self, instance: Any, owner: type) -> F:
        loader, value = self._get_value(instance, owner)
        if not loader:
            return cast(F, value)

        return loader(value)

    def __set__(self, instance: Any, value: F) -> None:
        assert self.name, "Field name is not provided"
        data = self._get_dict(instance)

        value = self._dump_value(value)
        data[self.name] = value


_T = TypeVar("_T")


class _SeqAttr(MutableSequence[_T]):
    data: List[Any]
    funcs: Tuple[Optional[Loader[_T]], Optional[Dumper[_T]]]

    def __init__(
        self,
        funcs: Tuple[Optional[Loader[_T]], Optional[Dumper[_T]]],
        data: List[Any],
        dict_method: str,
    ) -> None:
        self.funcs = funcs
        self.data = data
        self.dict_method = dict_method

    def _from_dict(self, o: Any) -> _T:
        loader = self.funcs[0]
        if loader:
            return loader(o)
        else:
            return cast(_T, o)

    def _from_dict_seq(self, o: Iterable[Any]) -> MutableSequence[_T]:
        loader = self.funcs[0]
        if loader:
            return [loader(i) for i in o]
        else:
            return list(o)

    def _to_dict(self, o: _T) -> Any:
        dumper = self.funcs[1]
        if dumper:
            return dumper(o)

        f = getattr(o, self.dict_method, None)
        if f:
            return f()

        return o

    def _to_dict_seq(self, o: Iterable[_T]) -> MutableSequence[_T]:
        dumper = self.funcs[1]
        if dumper:
            return [dumper(i) for i in o]

        ret = []
        for item in o:
            f = getattr(item, self.dict_method, None)
            if f:
                ret.append(f())
            else:
                ret.append(item)

        return ret

    def __len__(self) -> int:
        return len(self.data)

    @overload
    def __getitem__(self, i: int) -> _T:
        ...

    @overload
    def __getitem__(self, i: slice) -> MutableSequence[_T]:
        ...

    def __getitem__(self, i: Union[int, slice]) -> Union[_T, MutableSequence[_T]]:
        if isinstance(i, slice):
            return self._from_dict_seq(self.data[i])
        else:
            return self._from_dict(self.data[i])

    @overload
    def __setitem__(self, i: int, item: _T) -> None:
        ...

    @overload
    def __setitem__(self, i: slice, item: Iterable[_T]) -> None:
        ...

    def __setitem__(self, i: Union[int, slice], item: Union[_T, Iterable[_T]]) -> None:
        if isinstance(i, slice):
            if not isinstance(item, Iterable):
                raise TypeError("can only assign an iterable")
            self.data[i] = self._to_dict_seq(item)
        else:
            self.data[i] = self._to_dict(cast(_T, item))

    def __delitem__(self, i: Union[int, slice]) -> None:
        del self.data[i]

    def __repr__(self) -> str:
        return f"<_AttrList: {self.data!r}>"

    def insert(self, i: int, item: _T) -> None:
        self.data.insert(i, self._to_dict(item))


class SequenceAttr(ItemAttrBase[F]):
    """SequenceAttr is ItemAttr specialized for sequence.

    :param load: Convert value from the source dictionary item.
    :param dump: Convert assigned value to store to the source dictionary item.
    :param name: key in the source dictionary item. Default to attr name in class.
    :param default: Default value is the item is not exit in the source dictionary.

    Each elements in the sequence is converted by ``load``/``dump`` function on
    reading/writing the value.
    """

    def __get__(self, instance: Any, owner: type) -> MutableSequence[F]:
        _, value = self._get_value(instance, owner)

        return _SeqAttr[F](self.funcs, value, self.DICT_METHOD)

    def __set__(self, instance: Any, value: Sequence[F]) -> None:

        assert self.name, "Field name is not provided"
        data = self._get_dict(instance)

        values = [self._dump_value(v) for v in value]
        data[self.name] = values


_K = TypeVar("_K")
_V = TypeVar("_V")


class _MappingAttr(MutableMapping[_K, _V]):
    data: Dict[Any, Any]
    funcs: Tuple[Optional[Loader[_V]], Optional[Dumper[_V]]]

    def __init__(
        self,
        funcs: Tuple[Optional[Loader[_V]], Optional[Dumper[_V]]],
        data: Dict[Any, Any],
        dict_method: str,
    ) -> None:
        self.funcs = funcs
        self.data = data
        self.dict_method = dict_method

    def _from_dict(self, o: Any) -> _V:
        loader = self.funcs[0]
        if loader:
            return loader(o)
        else:
            return cast(_V, o)

    def _to_dict(self, o: _V) -> Any:
        dumper = self.funcs[1]
        if dumper:
            return dumper(o)

        f = getattr(o, self.dict_method, None)
        if f:
            return f()

        return o

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, k: _K) -> _V:
        return self._from_dict(self.data[k])

    def __setitem__(self, k: _K, item: _V) -> None:
        self.data[k] = self._to_dict(item)

    def __delitem__(self, k: _K) -> None:
        del self.data[k]

    def __repr__(self) -> str:
        return f"<_AttrDict: {self.data!r}>"

    def __iter__(self) -> Iterator[_K]:
        return iter(self.data)


K = TypeVar("K")
V = TypeVar("V")


class MappingAttr(Generic[K, V], ItemAttrBase[V]):
    """MappingAttr is ItemAttr specialized for mapping.

    :param load: Convert value from the source dictionary item.
    :param dump: Convert assigned value to store to the source dictionary item.
    :param name: key in the source dictionary item. Default to attr name in class.
    :param default: Default value is the item is not exit in the source dictionary.

    Each item value in the mapping is converted by ``load``/``dump`` function on
    reading/writing the value.

    Unlike ItemAttr, MappingAttr is a generic class with two type parameter for
    key and value.

    ::

        class Test(DictModel):
            mappingfield = MappingAttr[str, int]()  # mappingfield is Dict[str, int]
    """

    def __get__(self, instance: Any, owner: type) -> MutableMapping[K, V]:
        _, value = self._get_value(instance, owner)

        return _MappingAttr[K, V](self.funcs, value, self.DICT_METHOD)

    def __set__(self, instance: Any, value: MutableMapping[K, V]) -> None:
        assert self.name, "Field name is not provided"
        data = self._get_dict(instance)

        values = {k: self._dump_value(v) for k, v in value.items()}
        data[self.name] = values


class DictModel:
    """DictModel can be used to wrap dictionary object.

    :param values: Dictionary to wrap.

    DictModel class is not mandatory to use ItemAttr, but is provied to avoid boilerplate code.
    ItemAttr works any classes with ``__dictattr_get__()`` method.


    """

    values: Dict[str, Any]

    def __init__(self, values: Dict[str, Any]) -> None:
        self.values = values

    def __dictattr_get__(self) -> Dict[str, Any]:
        """Special method called by ItemAttr.
        Returns dictionary object to wrap."""

        return self.values
