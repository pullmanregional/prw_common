from typing import List
from datetime import datetime, time
from sqlalchemy.orm import registry
from sqlmodel import Field, Relationship
from .prw_meta_model import PrwMetaModel, PrwMeta, PrwSourcesMeta


class PrwModel(PrwMetaModel, registry=registry()):
    pass


class PrwPatient(PrwModel, table=True):
    __tablename__ = "prw_patients"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(
        unique=True,
        index=True,
        max_length=24,
        description="ID hash from unique salt and row ID",
    )
    sex: str = Field(regex="^[MFO]$")
    age: int | None = Field(description="Age in years")
    age_in_mo_under_3: int | None = Field(description="Age in months if <3yo")
    city: str | None = None
    state: str | None = None
    pcp: str | None = None


class PrwEncounter(PrwModel, table=True):
    __tablename__ = "prw_encounters"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(index=True, max_length=24)
    dept: str
    encounter_date: int = Field(
        description="Date of encounter in YYYYMMDD format as an integer"
    )
    encounter_time: str = Field(
        max_length=4, description="Time of encounter as HHSS in 24-hour format"
    )
    encounter_age: int | None = Field(description="Age in years at encounter")
    encounter_age_in_mo_under_3: int | None = Field(
        description="Age in months at encounter if <3yo"
    )
    encounter_type: str
    service_provider: str | None = None
    billing_provider: str | None = None
    with_pcp: bool | None = None
    appt_status: str | None = None
    diagnoses: str | None = None
    level_of_service: str | None = None


class PrwMyChart(PrwModel, table=True):
    __tablename__ = "prw_mychart"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(unique=True, index=True, max_length=24)
    mychart_status: str | None = None
    mychart_activation_date: int | None = Field(description="Int in YYYYMMDD format")
