from sqlalchemy.orm import registry
from typing import List
from sqlmodel import Field, SQLModel, Relationship
from datetime import date


class PrwIdModel(SQLModel, registry=registry()):
    pass


class PrwId(PrwIdModel, table=True):
    """
    Lookup table between prw_id and other unique patient IDs, like MRN
    """

    __tablename__ = "prw_ids"
    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(unique=True, index=True, max_length=24)
    mrn: str = Field(unique=True, index=True, max_length=24)
    details: List["PrwIdDetails"] = Relationship(back_populates="prw_id_ref")


class PrwIdDetails(PrwIdModel, table=True):
    __tablename__ = "prw_id_details"
    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(unique=True, index=True, max_length=24)
    mrn: str = Field(unique=True, index=True, max_length=24)
    name: str | None = None
    dob: date | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip: str | None = None
    phone: str | None = None
    email: str | None = None

    prw_id_ref: PrwId = Relationship(
        back_populates="details",
        sa_relationship_kwargs={"foreign_keys": "[PrwIdDetails.prw_id]"}
    )
