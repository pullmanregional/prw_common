from sqlalchemy.orm import registry
from sqlmodel import Field, SQLModel
from datetime import datetime


class PrwMetaModel(SQLModel, registry=registry()):
    pass


class PrwMeta(PrwMetaModel, table=True):
    __tablename__ = "prw_meta"
    id: int | None = Field(default=None, primary_key=True)
    dataset: str = Field(unique=True, max_length=1024, index=True)
    modified: datetime


class PrwSourcesMeta(PrwMetaModel, table=True):
    __tablename__ = "prw_sources_meta"
    id: int | None = Field(default=None, primary_key=True)
    source: str = Field(unique=True, max_length=1024, index=True)
    modified: datetime
