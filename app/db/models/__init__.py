import datetime
import enum
from typing import Annotated

from sqlalchemy import text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, mapped_column


# Создание базового класса для всех моделей
# Model = declarative_base()
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', NOW())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', NOW())"), onupdate=datetime.datetime.utcnow)]
str_256 = Annotated[str, mapped_column(String(256))]

class RoastingLevel(enum.Enum):
    filter = "фильтр"
    spro = "эспрессо"
    milk = "под молоко"


class Model(DeclarativeBase):
    type_annotation_map = {
        "intpk": intpk,
        "created_at": created_at,
        "updated_at": updated_at,
        "str_256": str_256
    }