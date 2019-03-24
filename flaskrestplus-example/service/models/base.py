import datetime
import enum
import typing

from sqlalchemy.orm import class_mapper

from service.models import database


class BaseModel(database.db.Model):
    __abstract__ = True

    def __init__(self, **kwargs: typing.Any) -> None:
        super(BaseModel, self).__init__(**kwargs)

    def to_dict(self, found: typing.Set = None) -> typing.Dict[str, typing.Any]:
        if found is None:
            found = set()

        mapper = class_mapper(self.__class__)
        columns = [column.key for column in mapper.columns]

        result = dict()
        for column in columns:
            if isinstance(getattr(self, column), type(datetime)):
                result[column] = getattr(self, column).isoformat()
            elif isinstance(getattr(self, column), enum.Enum):
                result[column] = getattr(self, column).name
            else:
                result[column] = getattr(self, column)

        for name, relation in mapper.relationships.items():
            if relation not in found:
                found.add(relation)
                related_obj = getattr(self, name)
                if related_obj is not None:
                    if relation.uselist:
                        result[name] = [child.to_dict(found) for child in related_obj]
                    else:
                        result[name] = related_obj.to_dict(found)

        return result
