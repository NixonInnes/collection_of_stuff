from pydantic import BaseModel
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Optional, Type


def create_model_from_table(
    Table: Type[DeclarativeMeta],
    BaseModel: Type[BaseModel] = BaseModel,
    skip_foreign_keys: bool = False,
) -> Type[BaseModel]:
    """Create a pydantic model from an SQLAlchemy table"""
    # Extract SQLAlchemy mapped attributes
    fields = {}
    for key, column in Table.__mapper__.all_orm_descriptors.items():
        # Only include columns, not relationships
        if not isinstance(column.property, ColumnProperty):
            continue

        # Skip foreign keys if skip_foreign_keys is True
        if skip_foreign_keys and column.foreign_keys:
            continue

        if column.nullable:
            type_ = Optional[column.type.python_type]
        else:
            type_ = column.type.python_type

        fields[key] = (type_, None if column.nullable else ...)


    Model = create_model(
        f"{Table.__name__}Model",
        **fields,
        __base__=BaseModel,
    )
    return Model
