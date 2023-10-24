from sqlalchemy import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import RelationshipProperty
from typing import List, Optional, Type


def is_relationship(column):
    """Check if a column is a relationship"""
    return isinstance(inspect(column).property, RelationshipProperty)

    
def traverse_tables(Table: Type[DeclarativeMeta], column_map: str, traversal: List = []):
    """Traverse a column map (i.e., attr.sub_attr.another_attr), returning each SQLAlchemy column in a list"""
    column_names = column_map.split(".")
    
    try:
        column = getattr(Table, column_names[0])
    except AttributeError as e:
        raise AttributeError(f"{Table} does not have attribute {column_names[0]}")
    
    traversal.append(column)
    
    if len(column_names) > 1:
        if not is_relationship(column):
            raise ValueError(f"{Table}.{column_names[0]} is not a relationship")

        sub_Table = column.property.mapper.class_
        return traverse_tables(sub_Table, ".".join(column_names[1:]), traversal)

    return traversal


def get_column_type(column):
    return inspect(column).type.python_type
