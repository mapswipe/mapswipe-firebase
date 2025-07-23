import typing
from datetime import datetime

from pydantic import BaseModel


@typing.overload
def serialize(
    obj: list,
) -> list: ...


@typing.overload
def serialize(
    obj: dict,
) -> dict: ...


@typing.overload
def serialize(
    obj: set,
) -> set: ...


@typing.overload
def serialize(
    obj: tuple,
) -> tuple: ...


@typing.overload
def serialize(
    obj: datetime,
) -> str: ...


@typing.overload
def serialize(
    obj: int,
) -> int: ...


@typing.overload
def serialize(
    obj: float,
) -> float: ...


@typing.overload
def serialize(
    obj: None,
) -> None: ...


@typing.overload
def serialize(
    obj: BaseModel,
) -> dict: ...


def serialize(
    obj: BaseModel | datetime | set | dict | list | tuple | int | float | bool | None,
):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize(i) for i in obj]
    if isinstance(obj, tuple):
        return tuple(serialize(i) for i in obj)
    if isinstance(obj, set):
        return {serialize(i) for i in obj}
    if isinstance(obj, BaseModel):
        return serialize(obj.model_dump(mode="python"))
    return obj
