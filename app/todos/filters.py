""" Filtering/sorting parameters are defined here
"""
import enum
from marshmallow import Schema, fields


class SortByEnum(enum.Enum):
    id = "id"
    done = "done"


class SortDirectionEnum(enum.Enum):
    asc = "asc"
    desc = "desc"


class ListTodosParameters(Schema):
    order_by = fields.Enum(SortByEnum, load_default=SortByEnum.id)
    order = fields.Enum(SortDirectionEnum, load_default=SortDirectionEnum.asc)
